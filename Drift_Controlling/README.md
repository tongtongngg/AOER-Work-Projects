# Drift Controlling

Genererer et Excel-overblik over **driftsomkostninger pr. projekt** i forhold til
løbende budget (LB), med difference i kr. og %, benchmarket mod hvor langt vi er
inde i året. Se `CLAUDE.md` for datamodel, kolonneopbygning og domæneviden.

## Layout

```
Drift_Controlling/
├── src/
│   ├── drift_controlling.py   ← selve scriptet (egen argparse-CLI)
│   └── main.py                ← kørselswrapper: stier + parametre ét sted
├── data/
│   ├── raw/<datasæt>/         ← inputfiler pr. kørsel (gitignored)
│   └── processed/             ← genererede Excel-filer
├── docs/                      ← PDF-spec + forventet output
└── notebooks/                 ← ad hoc-analyse
```

## Kørsel

Repoet er et uv-projekt, så afhængighederne håndteres af `uv run` fra repo-roden:

```bash
uv run python Drift_Controlling/src/main.py            # datasæt Test1, ultimo juni
uv run python Drift_Controlling/src/main.py --list     # vis tilgængelige datasæt
uv run python Drift_Controlling/src/main.py --dataset Test2 --month 9
uv run python Drift_Controlling/src/main.py --benchmark 0.42
```

Uden uv: `pip install -r requirements.txt` og kør `python src/main.py`.

`main.py` finder selv de to inputfiler i `data/raw/<datasæt>/` ud fra
filnavnsmønstrene `LB fil*` og `Projektstamdata*`, og skriver resultatet til
`data/processed/Drift_output_<datasæt>.xlsx`. Standardvalg (datasæt, måned,
mønstre) ligger som konstanter øverst i `main.py` — `drift_controlling.py`
skal ikke redigeres.

`drift_controlling.py` kan også køres direkte med eksplicitte stier:

```bash
uv run python Drift_Controlling/src/drift_controlling.py \
  --lb "..." --stamdata "..." --month 6 --output "..."
```

## Layoutgenkendelse

Inputfilernes layout bliver **genkendt**, ikke antaget: antallet af headerrækker
findes ud fra kolonnenavnene, første datalinje ud fra hvor de rigtige tal starter,
og kolonnerne matches på navn med positionerne fra specen som reserve. Det gør
kørslen robust over for OTBI/OAC-eksporter med et andet antal headerrækker.

Bliver et kolonnenavn ikke genkendt, bruges reservepositionen, og kørslen skriver
til sidst:

```
ADVARSLER:
  ! LB fil.csv: kolonnenavnet for 'actual' blev ikke genkendt - bruger position I ...
```

**Advarsler skal læses.** De betyder at layoutet afviger fra specen, og at outputtet
bør kontrolleres før det sendes videre. Ingen advarsler = alle kolonner genkendt.

## Validering

Datasættet `Test1` med `--month 6` skal give 59 LB-detailrækker → 44 driftsrækker
→ 14 outputlinjer og 1 linje på fanen `Fravalgt`, uden advarsler.

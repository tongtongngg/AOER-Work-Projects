# Intrastat-assistent

Denne mappe indeholder `runme.py`, et script, der er beregnet til at blive
uploadet til en Microsoft Copilot-agent sammen med månedens Excel-projektmapper.
Agenten bruger scriptet til at klargøre en dansk Intrastat-importprojektmappe,
identificere rækker, der skal gennemgås, og hjælpe med at finde gyldige
varekoder til varer uden en brugbar kode.

Se [`agent-instructions.md`](agent-instructions.md) for agentens detaljerede
arbejdsgang og krav til svar.

## Hvad agenten gør

Arbejdsgangen består af to trin:

1. **Klargør månedsrapporten.** Agenten kører `runme.py run`. Scriptet læser
   Fusion-eksporten og Intrastat-skabelonen, anvender eventuel brugbar
   leverandørhistorik og fakturainformation og opretter rapporten og
   gennemgangsfilerne. Rækker klassificeres som klar til brug, service,
   udelukket eller kræver gennemgang.
2. **Undersøg manglende varekoder.** For gennemgangsrækker, der mangler en kode,
   undersøger agenten produktet ved hjælp af fakturainformation og
   leverandørdokumentation. Derefter kontrollerer den mulige 8-cifrede koder
   mod skabelonens ark `Opslag` ved hjælp af `runme.py codes`. Agenten
   registrerer de undersøgte beslutninger og kører `runme.py apply` for at
   genopbygge outputfilerne ud fra de oprindelige inputfiler.

Rækker, der kræver manuel behandling af andre årsager end en manglende kode —
for eksempel et manglende land eller en manglende DKK-værdi — rapporteres til
brugeren i stedet for at blive udfyldt ved gæt. Agenten må kun anvende koder,
som scriptets `codes`-hjælpefunktion returnerer, og skal angive kilde og
sikkerhedsniveau for undersøgte beslutninger.

## Filer, der skal stilles til rådighed

Upload `runme.py` og månedens projektmapper til Copilot-agenten:

- **Påkrævet:** Månedens Fusion Intrastat-eksport.
- **Påkrævet:** Intrastat-skabelonprojektmappen (`.xlsm`; filnavnet indeholder
  `skabelon`, og den indeholder arket `Opslag` med gyldige koder).
- **Anbefalet:** `LEV-HSKoder.xlsx`, som indeholder historik over leverandørernes
  varekoder. Uden denne fil kan scriptet ikke bruge eller opdatere historikken.
- **Anbefalet:** `Fakturaer YYYY-MM.xlsx`, som indeholder fakturalinjer, der kan
  hjælpe med at identificere produkter og supplerende mængder. Uden denne fil
  er disse oplysninger ikke tilgængelige.
- **Valgfrit:** En CSV-fil eller Excel-projektmappe med tilsidesættelser, hvis
  der er behov for specifikke fakturakorrektioner.

Agentens instruktioner forudsætter, at filerne er tilgængelige i `/mnt/data`.
Hvis en påkrævet projektmappe mangler, eller scriptet ikke kan identificere den
korrekte fil, skal agenten bede om den manglende fil eller bruge eksplicitte
filstier i stedet for at gætte.

## Brug af agenten

1. Upload `runme.py` og månedens filer som beskrevet ovenfor.
2. Bed agenten om at klargøre månedens Intrastat-rapport. Agenten udfører det
   indledende `run`-trin og giver links til den oprettede projektmappe og
   gennemgangsfilerne.
3. Hvis der mangler koder, undersøger agenten kun de gennemgangsposter, der
   mangler koder, validerer hver mulig kode mod `Opslag` og anvender de
   godkendte beslutninger. Gennemgå eventuelle afventende beslutninger med lavt
   sikkerhedsniveau og rækker til manuel behandling, før rapporten betragtes
   som færdig.
4. Bekræft eller korrigér eventuelle afventende beslutninger sammen med
   agenten. Den kan genopbygge outputfilerne ud fra de oprindelige inputfiler
   ved hjælp af `apply`.

Agentens detaljerede instruktioner findes i
[`agent-instructions.md`](agent-instructions.md). Følg dem for at se den
præcise kørselsprocedure og hvordan du får links til outputfilerne.

## Outputfiler

Filerne skrives til den outputmappe, der angives til scriptet (agentens
instruktioner bruger `/mnt/data`):

- `Intrastat_YYYY-MM.xlsm` — oprettet rapportprojektmappe baseret på den
  medfølgende skabelon.
- `Intrastat_review_YYYY-MM.xlsx` og `.json` — gennemgangsrækker, årsager,
  supplerende fakturainformation og undersøgte kodebeslutninger.
- `LEV-HSKoder_YYYY-MM.xlsx` — opdateret historik over leverandørkoder, hvis
  der blev leveret en inputfil med historikken.
- `Intrastat_log_YYYY-MM.json` — kørselsoversigt, antal, placeringer af input-
  og outputfiler samt (efter `apply`) anvendte, afventende og afviste
  beslutninger.
- `Intrastat_run_YYYY-MM.json` — manifest, der gemmes af `run` og bruges af
  `apply` til at genopbygge outputfilerne ud fra de samme oprindelige
  inputfiler.

## Håndtering af beslutninger

`apply` validerer, at beslutningerne vedrører fakturaer i gennemgangen, som
mangler en kode, og at hver varekode, der ikke gælder en service, er en gyldig
8-cifret kode i `Opslag`. Ugyldige beslutninger afvises og rapporteres.
Varekoden `"0"` angiver, at en faktura vedrører en service.

Som standard anvender `apply` beslutninger med lavt sikkerhedsniveau sammen med
andre gyldige beslutninger. Brug `--hold-low` for at lade koder med lavt
sikkerhedsniveau (og servicedecisioner med middel sikkerhedsniveau) forblive
afventende i gennemgangen. Agenten skal tydeligt angive dette valg og bede
brugeren bekræfte de beslutninger, der fortsat afventer.

Outputtet er en klargjort rapport og erstatter ikke en gennemgang af
klassificeringen og den endelige projektmappe.

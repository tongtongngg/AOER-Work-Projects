# DTU Automatisk Driftcontrolling (Bottom Up)

Dette værktøj er designet til at gøre controlling af drift langt lettere. Det tager de rå-data fra Fusion og sammenstiller automatisk løbende budget og faktisk forbrug pr. projekt og udgiftskategori. Derudover holder det forbruget op mod, hvor langt vi er nået på året, så du med det samme kan se, om et projekt er på vej til at overskride sit driftsbudget — uden manuelle beregninger.

**Forarbejdet af:** *(indsæt navn og enhed)*

## Formål

Værktøjet automatiserer de centrale beregninger i forbindelse med driftscontrolling:

- Den samler løbende budget og actuals pr. projekt og udgiftskategori i ét overblik.
- Difference i både kr. og procent, så over- og underforbrug er umiddelbart synligt.
- Benchmark mod årets forløb: den beregner en forventet justering ud fra, hvor langt vi er på året.
- Automatisk frasortering af alt, der ikke er drift (løn, overhead, tilskud m.m.).
- Identifikation af datamæssige problemer og fravalgte projekter (FRAVALGT)
- Visuel formatering (rød markering ved merforbrug, talformatering m.m.)

---

<br>

## Baggrund

Hverken Fusion eller EPM kan i dag levere det samlede overblik i én rapport. Løbende budget og actuals ligger i én rapport, mens sektionsnummer, projektcontroller og projektperiode ligger i en anden. Derfor kombinerer værktøjet to udtræk til ét output.

---

<br>

## Brugervejledning

For at Copilot Agenten kan behandle din driftcontrolling har den brug for **tre input**: én Python-fil, to rådatafiler — og den måned, opgørelsen dækker.

### **1. RUNME.py (Python-behandlingsfil)**
Agenten bruger denne fil til at udføre alt beregning og formattering.

Download RUNME.py her:

> **[Download seneste version](INDSÆT_LINK_TIL_RELEASE)**


### **2. Rådata fra Fusion (CSV-format) — to filer**

Begge rapporter trækkes fra Fusion som CSV-filer.

**a) "LB-filen" — Projektstatus, løbende budget**

> Project Controller Reports → Projektstatus → Fusion Rapporter (OTBI) (Projektstatus) → **Projektstatus – løbende budget**
>
> Vælg: Projektorganisation · indeværende år · **ultimo kalendermåned** · alle projektnavne · **niveau 2**
>
> Hentes under Eksporter → Formater → CSV

**b) "Projektstamdatafilen" — Projektstamdata**

> Project Controller Reports → Projektstamdata → OAC Rapporter (Projektstamdata)
>
> Vælg: Project Organization · Projektstatus = **Active**
>
> Hentes som CSV

En download-guide med billeder samt hele brugervejledningen findes her:

> **[Download seneste vejledning](INDSÆT_LINK_TIL_VEJLEDNING)**


*OBS:* Filerne skal eksporteres som **CSV**, ikke Excel.


### **3. Måned (nyt input)**

Værktøjet skal vide, hvor langt vi er på året, for at kunne beregne benchmark og justering. Det kan ikke læses ud af rådataen, så **du skal selv oplyse måneden** i beskeden til agenten.

Benchmark beregnes som **månedens nummer / 12**:

| Ultimo måned | Benchmark |
| :--- | :--- |
| marts | 3/12 = 0,25 |
| maj | 5/12 = 0,42 |
| juni | 6/12 = 0,50 |
| september | 9/12 = 0,75 |

> [!WARNING]
> Måneden skal svare til den **ultimo kalendermåned**, du valgte i LB-udtrækket. Vælger du fx juni i Fusion, men skriver september til agenten, bliver alle justeringer forkerte — og der er intet i filerne, der kan afsløre fejlen.

---

## Sådan bruger du værktøjet i Copilot-agenten

1.  **Åbn Copilot-agenten:** Vælg agenten **DTU Automatisk Driftcontrolling**.
2.  **Upload filer:** Vedhæft **begge CSV-filer** og **RUNME.py** i den samme besked.
3.  **Aktiver processen:** Skriv følgende kommando i chatten, med din måned indsat:

    ---
    ### **`Kør driftcontrolling for juni.`**
    ---

    > *OBS: Vent på, at alle tre filer er færdiguploadet i Copilot-chatten, før du sender beskeden.*

    > **Fejlhåndtering:**
    > Hvis du får en fejlbesked om, at "RUNME.py ikke er indlæst korrekt" eller kun er delvist indlæst, så skriv: **"Indlæs RUNME og begge CSV-filer fuldt og kør igen"**. Hvis den stadig fejler, så åbn en ny chat og prøv igen.

4.  **Vent på behandlingen:** Når du har sendt beskeden, håndterer agenten automatisk resten:
    * **Databehandling:** Agenten læser filerne og afvikler Python-koden.
    * **Kvalitetstjek:** Systemet sikrer, at dataene er korrekt behandlet, og advarer hvis filernes layout har ændret sig.
    * **Resultat:** Du modtager et direkte download-link til din færdige Excel-fil.
---

> [!IMPORTANT]
> **Bemærk venligst følgende ved generering:**
>
> **Behandlingstid:** Det tager typisk et par minutter for agenten at færdiggøre beregningerne. Forlad ikke siden, før processen er afsluttet.
>
> **Platform:** Hvis du oplever fejl med Excel-downloadlinket i Microsoft Teams, skal du køre agenten direkte i en webbrowser.
>
> **Teams download:** Hvis du kører agenten gennem Teams, fører download-linket til en Excel-fil på SharePoint i din browser, uden at downloade automatisk.
Hvis du gerne vil have den downloadet på din enhed, skal du trykke på File → Create a Copy → Download a Copy.

## Link til Copilot Agenten for automatisk behandling
> **[Copilot Agent link](INDSÆT_LINK_TIL_AGENT)**

*OBS:* Virker kun for medarbejdere og studerende med en DTU-mail

<br>


## Funktioner

Værktøjet behandler de to udtræk fra Fusion og genererer automatisk følgende:

* **Samlet driftsoverblik:** Én linje pr. projekt, underkonto og udgiftskategori med løbende budget, actuals og difference i kr.
* **Forbrugsprocent:** Viser hvor stor en andel af det løbende budget der er brugt.
* **Beregnet justering:** Fremskriver forbruget til helårsniveau ud fra benchmark og viser, hvor meget budgettet i givet fald mangler.
* **Rød markering:** Linjer med merforbrug markeres automatisk med rød skrift.
* **Fravalgte projekter:** Opretter et separat ark til projekter, der ikke indgår i output — fx projekter uden driftsomkostninger, eller projekter der mangler i det ene af de to udtræk.
* **Justerbar benchmark:** Benchmark ligger i én gul inputcelle på arket "Forudsætninger". Ændrer du den, genberegnes hele arket i Excel — du behøver ikke køre agenten igen.

### Ark i outputfilen

| Ark | Indhold |
| :--- | :--- |
| **Forudsætninger** | Benchmark (gul inputcelle), kildefiler, kørselsdato og forklaring af formlerne |
| **Drift** | Selve overblikket, kolonne A–O |
| **Fravalgt** | Projekter der er sorteret fra, med begrundelse |

---

## Arbejdsgang

1.  **Udtræk:** Lav de to dataudtræk fra Fusion (LB-fil og Projektstamdata).
2.  **Behandling:** Kør værktøjet med de to udtræk som input, og oplys måneden.
3.  **Gennemgang:** Analyser arket "Drift" for over- og underforbrug, og tjek "Fravalgt" for projekter der kræver opmærksomhed.
4.  **Kommentering:** Udfyld kolonne "Kommentar YTD" med jeres vurdering af de linjer, der skiller sig ud.

---

## Teknisk Logik

| Funktion | Beskrivelse |
| :--- | :--- |
| **Driftskategorier** | Kun disse fire medtages: *Intern produktion mv., køb* · *Lejeomkostninger o.l.* · *Rejser og repræsentation* · *Øvrige omkostninger*. Løn, overhead, tilskud m.m. frasorteres. |
| **Styrende fil** | LB-filen er styrende. Projekter der kun findes i Projektstamdata, kommer ikke i output, men vises på arket "Fravalgt". |
| **Sammenlægning** | Beløb lægges sammen pr. projekt, underkonto (UK) og udgiftskategori. Ét projekt med tre driftskategorier fylder tre linjer. |
| **Benchmark** | Beregnes som: $\text{Månedens nummer} / 12$ |
| **Difference** | Beregnes som: $\text{Løbende budget} - \text{Actuals}$. Negative tal = merforbrug og markeres rødt. |
| **Difference \%** | Beregnes som: $\text{Actuals} / \text{Løbende budget}$, dvs. forbrugsprocent. |
| **Beregnet justering** | Beregnes som: $\text{Actuals} / \text{Benchmark} - \text{Løbende budget}$ |
| **LB = 0** | Linjer uden løbende budget markeres automatisk i kolonnen "Kommentar YTD" og skal vurderes manuelt. |
| **Sektionsnummer** | Udledes automatisk af projektorganisationen i Projektstamdata (de fire cifre). |
| **Datafejl** | Projekter uden driftskategorier, eller som mangler i det ene udtræk, flyttes automatisk til arket "Fravalgt". |

---

## Kendte forhold ved aflæsning

> [!NOTE]
> **Modposteringer på eksternt finansierede projekter.** På EU-projekter o.l. bogføres medfinansiering med modsatrettede beløb på to underkonti. De udligner hinanden, men står som to linjer i output. Læs derfor projektets underkonti samlet, før du konkluderer på en enkelt linje.
>
> **Forskel i udgiftskategori.** Er budgettet lagt på én udgiftskategori, mens forbruget er bogført på en anden, fremstår den ene linje som merforbrug og den anden som mindreforbrug med samme beløb. Her er den rigtige handling en **omkontering** — ikke en budgetjustering.

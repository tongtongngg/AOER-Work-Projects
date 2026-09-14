# DTU Debitoragent (Matchning af indbetalinger uden fakturareference)

Dette værktøj er designet til at gøre arbejdet med uidentificerede indbetalinger langt lettere. Det læser bankens betalingsadvis, udtrækker afsender, beløb, valuta, dato og meddelelse til modtager, og undersøger derefter DTU's egne kilder og åbne kilder for at finde ud af, hvilket projekt og hvilken modtager betalingen hører til. Resultatet er et struktureret, kildeunderbygget forslag, som en controller kan kontrollere — i stedet for manuel søgning på tværs af systemer.

**Forarbejdet af:** *(indsæt navn og enhed)*

## Formål

Værktøjet automatiserer det udredningsarbejde, der ligger forud for konteringen:

- Udtrækker afsender, beløb, valuta, dato, betalingsmeddelelse og eventuelle referencer fra bankmeddelelsen.
- Vurderer betalingens karakter — fx forskningsmidler, fondsbetaling, royalty eller almindelig debitorbetaling.
- Undersøger projektnavne, akronymer, bevillinger og publikationer for at knytte betalingen til et konkret projekt.
- Finder en sandsynlig faglig kontakt og det relevante institut på DTU.
- Slår den tilknyttede projektøkonom og Project Finance Manager op i **[Organisationsdiagram – Projektøkonomi](https://dtudk.sharepoint.com/sites/AR-trden/_layouts/15/Doc.aspx?sourcedoc=%7B27291C98-7E80-4BC0-BFD1-73B357990857%7D&file=Organisationsdiagram%20-%20Projekt%C3%B8konomi.pptx&action=edit&mobileredirect=true&DefaultItemOpen=1)**.
- Præsenterer resultatet som ét samlet forslag med kilde på hver oplysning.

> [!IMPORTANT]
> **Agenten foretager ikke den endelige kontering eller bogføringsbeslutning.** Den leverer et dokumenteret forslag. Beslutningen ligger hos controlleren.

---

<br>

## Baggrund

En del indbetalinger til DTU kommer ind uden fakturareference. Afsenderen er typisk en udenlandsk universitetspartner, en fond eller en forlagsudbetaling, og eneste spor er en kort betalingsmeddelelse med et projektakronym, et bevillingsnummer eller et navn. Oplysningerne, der skal til for at placere betalingen, ligger spredt: projekt- og kundedata i DTUDOCX, forskningsprojekter og publikationer i DTU Orbit, bevillingsdata hos bevillingsgiveren, og ansvarsfordelingen i organisationsdiagrammet for Projektøkonomi. Agenten samler den søgning i én arbejdsgang.

---

<br>

## Brugervejledning

For at agenten kan behandle en betaling har den brug for **ét input**: oplysningerne om indbetalingen.

### **1. Betalingsadvis (PDF) — anbefalet**

Vedhæft bankens betalingsadvis direkte i chatten. Agenten læser selv afsender, beløb, valuta, dato og meddelelse til modtager ud af dokumentet.

### **2. Eller indsat tekst**

Har du ikke adviset som fil, kan du indsætte oplysningerne manuelt. Jo mere du kan give, jo bedre bliver matchet:

| Oplysning | Betydning for matchet |
| :--- | :--- |
| **Afsender** | Vigtigste spor — identificerer partner, fond eller forlag |
| **Beløb og valuta** | Bruges til at genkende tranche- og ratebetalinger |
| **Dato** | Bruges til at holde betalingen op mod projektperiode og bevillingsplan |
| **Meddelelse til modtager** | Indeholder ofte akronym, bevillings-ID eller navn |
| **Øvrige referencer** | Fx kontrakt-, ordre- eller bevillingsnummer |

> [!WARNING]
> Betalingsmeddelelsen er ofte afkortet af banken. Hvis du indsætter oplysningerne manuelt, så **gengiv meddelelsen ordret** — også hvis den ser ud som volapyk. Et afkortet akronym eller et halvt bevillingsnummer er tit netop det, der afgør matchet.

### **3. Supplerende oplysninger (valgfrit)**

Ved du allerede noget — fx at betalingen formodes at høre til et bestemt institut, eller at der tidligere er kommet en tilsvarende betaling fra samme afsender — så skriv det med. Agenten bruger det som udgangspunkt for søgningen.

---

## Sådan bruger du værktøjet i Copilot-agenten

1.  **Åbn Copilot-agenten:** Vælg agenten **DTU Debitoragent**.
2.  **Upload betalingsadviset:** Vedhæft PDF'en — eller indsæt oplysningerne som tekst.
3.  **Aktiver processen:** Skriv følgende kommando i chatten:

    ---
    ### **`Match denne betaling.`**
    ---

    > *OBS: Vent på, at filen er færdiguploadet i Copilot-chatten, før du sender beskeden.*

    > **Fejlhåndtering:**
    > Hvis agenten svarer, at den ikke kan læse adviset, eller kun har fået fat i dele af det, så skriv: **"Læs betalingsadviset fuldt igen og gengiv afsender, beløb, valuta, dato og meddelelse til modtager, før du søger"**. Hjælper det ikke, så indsæt oplysningerne som tekst i stedet, eller åbn en ny chat og prøv igen.

4.  **Vent på behandlingen:** Agenten håndterer resten:
    * **Udtræk:** Betalingens oplysninger læses ud af adviset.
    * **Klassifikation:** Betalingens karakter vurderes (forskningsmidler, fond, royalty, almindelig debitor).
    * **Søgning:** DTU's kilder og åbne kilder gennemsøges for projekt, institut og kontaktperson.
    * **Resultat:** Du modtager et struktureret forslag med kilde på hver oplysning.
5.  **Kontrollér forslaget:** Gennemgå kilderne, og træf selv beslutningen om kontering.

> [!NOTE]
> **Agenten har to tilstande.** Matchningsforløbet ovenfor udløses kun, når du vedhæfter et betalingsadvis eller indsætter betalingsoplysninger. Stiller du et almindeligt spørgsmål — fx om en proces, et projekt eller hvem der er projektøkonom på en enhed — svarer agenten helt normalt uden at gå i gang med et match.

---

> [!IMPORTANT]
> **Bemærk venligst følgende ved kørsel:**
>
> **Behandlingstid:** Søgningen på tværs af kilder tager typisk et par minutter. Forlad ikke siden, før forslaget er færdigt.
>
> **Platform:** Oplever du fejl med opslag i de interne kilder gennem Microsoft Teams, så kør agenten direkte i en webbrowser.
>
> **Adgang:** Opslag i DTUDOCX sker i din egen autentificerede browsersession. Agenten skriver ikke i systemerne — den henter og sammenstiller.

## Link til Copilot Agenten

> **[Copilot Agent link](INDSÆT_LINK_TIL_AGENT)**

*OBS:* Virker kun for medarbejdere og studerende med en DTU-mail

<br>

## Funktioner

Agenten behandler betalingsadviset og genererer automatisk følgende:

* **Udtrukne betalingsoplysninger:** Afsender, beløb, valuta, dato, betalingsmeddelelse og referencer, gengivet som de står i adviset.
* **Vurdering af betalingstype:** Forskningsmidler, fondsbetaling, royalty eller almindelig debitorbetaling — med begrundelse.
* **Projektidentifikation:** Søgning på projektnavne, akronymer, bevillinger og publikationer for at pege på det konkrete projekt.
* **Faglig kontakt og institut:** Sandsynlig modtager på DTU, med angivelse af hvor sandsynligheden kommer fra.
* **Økonomiansvarlige:** Projektøkonom og Project Finance Manager slås op i organisationsdiagrammet for Projektøkonomi.
* **Kildeunderbygning:** Hver oplysning i forslaget er forsynet med kilde, så controlleren kan efterprøve den i stedet for at tage den på tro.
* **Usikkerhedsmarkering:** Er grundlaget tyndt, siger agenten det — frem for at vælge den mest sandsynlige kandidat og præsentere den som sikker.

### Indhold i forslaget

| Afsnit | Indhold |
| :--- | :--- |
| **Betalingen** | De udtrukne oplysninger fra adviset, gengivet ordret |
| **Vurdering** | Betalingens karakter og begrundelsen for den |
| **Match** | Foreslået projekt, institut og faglig kontakt, med kilde |
| **Ansvarlige** | Projektøkonom og Project Finance Manager for enheden |
| **Kilder** | Samlet oversigt over de kilder, forslaget bygger på |
| **Forbehold** | Hvad agenten ikke kunne afklare, og hvad controlleren selv skal tjekke |

---

## Arbejdsgang

1.  **Modtag:** Hent bankens betalingsadvis på den uidentificerede indbetaling.
2.  **Behandling:** Kør agenten med adviset som input.
3.  **Gennemgang:** Kontrollér forslagets kilder — særligt projektidentifikationen og den faglige kontakt.
4.  **Bekræftelse:** Kontakt om nødvendigt projektøkonomen eller den faglige kontakt for at få matchet bekræftet.
5.  **Kontering:** Træf selv beslutningen og foretag konteringen i Fusion.

---

## Teknisk Logik

| Funktion | Beskrivelse |
| :--- | :--- |
| **Udtræk fra advis** | Afsender, beløb, valuta, dato, meddelelse til modtager og øvrige referencer læses ud af PDF'en eller den indsatte tekst. |
| **Klassifikation** | Betalingen henføres til én af fire typer: *forskningsmidler* · *fondsbetaling* · *royalty* · *almindelig debitorbetaling*. Typen styrer, hvilke kilder der søges i først. |
| **Interne kilder** | **DTUDOCX** (projekt- og kundedata) og **DTU Orbit** (forskningsprojekter, bevillinger og publikationer). |
| **Åbne kilder** | Bevillingsgiveres egne projektdatabaser, fondsoversigter og publikationsdata, når de interne kilder ikke er tilstrækkelige. |
| **Ansvarsopslag** | Projektøkonom og Project Finance Manager udledes af enheden via *Organisationsdiagram – Projektøkonomi*. |
| **Trancher** | Beløb sammenholdes med bevillingens rate- og tranchestruktur, så delbetalinger genkendes som delbetalinger. |
| **Gating** | Matchningsforløbet udløses kun ved vedhæftet advis eller indsatte betalingsoplysninger. Øvrige spørgsmål besvares normalt. |
| **Human-in-the-loop** | Agenten skriver ikke i økonomisystemerne. Alle opslag sker læsende, i en session autentificeret af brugeren. |
| **Kildekrav** | Oplysninger uden kilde medtages ikke i forslaget. Kan et led ikke dokumenteres, markeres det som uafklaret. |

---

## Kendte forhold ved aflæsning

> [!NOTE]
> **Akronymer er ikke entydige.** Projektakronymer går igen på tværs af programmer og institutioner, og det samme akronym kan dække flere bevillinger. Kontrollér altid, at det foreslåede projekt også passer på beløb, valuta og periode — ikke kun på navnet.
>
> **Afsender er ikke altid bevillingsgiver.** På EU- og konsortieprojekter kommer betalingen typisk fra koordinatoren, ikke fra bevillingsgiveren. Agenten peger på afsenderen som den fremgår af adviset; det underliggende projekt kan ligge et andet sted.
>
> **Faglig kontakt er et forslag, ikke en bekræftelse.** Kontaktpersonen udledes af projekt- og publikationsdata, som kan være forældede, hvis medarbejderen er fratrådt eller projektet har skiftet ansvarlig. Bekræft hos instituttet eller projektøkonomen, før betalingen konteres.
>
> **Royaltybetalinger mangler ofte projekttilknytning.** Forlagsudbetalinger kan være samlebetalinger for flere publikationer og har ikke nødvendigvis ét projekt at lande på. Her er den rigtige handling typisk en afklaring med instituttet — ikke et tvunget match.

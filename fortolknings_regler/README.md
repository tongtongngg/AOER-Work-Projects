# Fortolkning – web- og PDF-indsamling

Dette modul gennemløber *Inside* for at finde og indsamle alle fortolkningsregler.

Processen starter på den hjemmeside, der er defineret i `inside_to_pdf_fortolkning`. Herfra udføres en **BFS (Breadth-First Search)**, hvor alle relevante sider besøges, og indholdet gemmes som Markdown-filer (`.md`).  
Derudover downloades og gemmes alle PDF-filer, som der refereres til fra de enkelte sider.

Når hele processen er gennemført, har man en samling filer, som tilsammen dækker alle fortolkningsregler.

***

## Sådan køres modulet

### 1. Forberedelse

Sørg først for at installere alle nødvendige pakker.

### 2. Kør scripts i rækkefølge

Kør herefter følgende kommandoer i denne rækkefølge:

```bash
python main_fortolkning.py gather
python main_fortolkning.py combine_webpage
python main_fortolkning.py pdf_to_md
```

***

## Manuel efterbehandling (vigtigt)

Efter de tre scripts er kørt, anbefales det at gennemgå Markdown-filerne, der er genereret fra PDF’erne:

*   Nogle PDF’er kan være meget lange og bør evt. ligge i deres **egne filer** frem for at blive kombineret med øvrigt indhold.
*   Der findes endnu ikke et script til automatisk oprydning i `.md`- eller PDF-filerne.
*   Den nuværende PDF → Markdown-konvertering håndterer ikke altid billeder optimalt.

Derfor er **noget manuelt arbejde nødvendigt**.  
En praktisk løsning er at give PDF’en direkte til en LLM og få den konverteret til Markdown – det kræver dog, at modellen promptes korrekt.

***

## Samling af PDF-indhold

Når den manuelle oprydning er foretaget, kan følgende kommando køres:

```bash
python main_fortolkning.py combine_pdf
```

Herefter har du alle nødvendige filer klar til at blive brugt som input til din AI-agent.

***

## TODO

*   Find eller implementér en bedre og mere robust løsning til konvertering fra PDF til Markdown.

***



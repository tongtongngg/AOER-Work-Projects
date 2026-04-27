Dette modul kører igennem Inside for at finde alle fortolkningsreglerne. Den starter på den hjemmeside der er defineret i inside_to_pdf_fortolkning og laver ellers BFS fra denne side og henter alt information ned på md filer. Derudover gemmer den også PDFer der bliver ref til på de forskellige sider. 

Efter at have kørt det hele har man altså en håndful filer der sammen skulle dække alle fortolkningsregler.

Måden det skal kører på er følgende.
Download nødvendige pakker
Kør derefter:
python main_fortolkning.py gather
python main_fortolkning.py combine_webpage 
python main_fortolkning.py pdf_to_md
Efter at have kørt disse 3 kan det være smart lige at kigge md filerne fra pdferne igennem da nogle af dem kan være meget lange, og måske egentlig helst skulle være seres egen fil og ikke kombinerers med de andre. Derudover er der ikke udviklet noget script endnu til at rydde op i md/pdf filerne og det nuværende script kan ikke altid konverterer billeder på pdfer ordentligt til md så lidt manuelt arbejde er nødvendigt. Man kan bare give pdfen til en llm og få den til at konverterer det til en md fil for en men man skal lige prompte den ordentligt.
Efter dette er gjort kan man køre 
python main_fortolkning.py combine_pdf 
og man har nu alle nødvendige filer til at fodre sin AI agent med.

Lille to do. Ryd lidt mere op i filerne, inklusiv at gøre denne readme lidt bedre. find på en bedre løsning til at få omdannet pdf til md.
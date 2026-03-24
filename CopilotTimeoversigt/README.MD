# DTU Automatisk Timeoversigt

Dette værktøj behandler dataudtræk fra Fusion for automatisk at beregne og fordele medarbejdertimer. Det giver et optimeret overblik over normtid, planlægningsgrader og sektionsopdelte opsummeringer.


## Formål

Værktøjet automatiserer de centrale beregninger i forbindelse med timeoversigter:

- Beregning af normtid pr. medarbejder  
- Planlægningsgrader  
- Fordeling af timer på UK-koder  
- Automatisk opsummering pr. sektion  
- Identifikation af datamæssige problemer (DATA ISSUES)  
- Visuel formatering (trafiklys, talformatering m.m.)

---

## Brugervejledning

For at Copilot Agenten kan behandle din timeoversigt har den brug for to filer som du skal uploade i chatten. 

### **1. Rådata fra Fusion (CSV-format)**  
Python-scriptet, som udfører al behandling, beregning og formatering.

Download RUNME.py her:
[![Download RUNME.py](https://img.shields.io/badge/Download-RUNME.py-blue?style=for-the-badge&logo=python&logoColor=white)](https://raw.githubusercontent.com/tongtongngg/AOER-Work-Projects/main/CopilotTimeoversigt/RUNME.py)


### **2. RUNME.py (Python-behandlingsfil)**  
Agenten bruger denne fil til at udføre al beregning og formatlogik.
Download vejledning til at trække data fra Fusion:

*OBS:* Filen skal eksporteres som **CSV**, ikke Excel.


---


## Sådan bruger du værktøjet i Copilot Agenten

1. Åbn Copilot Agenten: *DTU Automatisk Timeoversigt*.  
2. Upload **CSV-filen** og **RUNME.py** i samme besked.  
3. Skriv:  
   **“Kør timeoversigten.”**  
4. Vent på, at agenten:  
   - Læser begge filer  
   - Kører Python-koden  
   - Genererer din Excel-fil  
   - Foretager kvalitetstjek  
   - Returnerer download-linket

*OBS:* Det kan tage et par minutter for Copilot agenten at generere timeoversigten. 

---


## Link til Copilot Agenten for automatisk behandling



## Funktioner

Værktøjet behandler udtræk fra Fusion og genererer automatisk følgende:

* **Beregnet normtid:** Beregner normtid pr. medarbejder baseret på ansættelsesgrad i Fusion og antallet af måneder, medarbejderen er ansat i det nuværende år. Der afrundes til halve måneder.
* **Planlægningsgrad:** Beregner de planlagte timer i forhold til medarbejderens normtid.
* **Fordeling på underkonti:** Fordeler de planlagte timer på underkonti i både faktiske tal og procentvis fordeling.
* **Sektionsoverblik:** Genererer et ark, hvor data er summeret op pr. sektion.
* **Fejlhåndtering (Data Issues):** Opretter et separat ark til eventuelle datafejl, f.eks. hvis en ansættelsesgrad mangler i systemet.

---

## Arbejdsgang

1.  **Udtræk:** Lav et hurtigt dataudtræk fra Fusion.
2.  **Behandling:** Kør værktøjet med det rå dataudtræk som input.
3.  **Gennemgang:** Analyser de genererede ark for sektionsoverblik og individuelle opgørelser.

---

## Teknisk Logik

| Funktion | Beskrivelse |
| :--- | :--- |
| **Afrunding** | Ansættelseslængde afrundes til nærmeste 0,5 måned. |
| **Normtid** | Beregnes som: $\text{Ansættelsesgrad} \times \text{Måneder ansat}$ |
| **Datafejl** | Rækker med manglende stamdata flyttes automatisk til arket "Data Issues". |


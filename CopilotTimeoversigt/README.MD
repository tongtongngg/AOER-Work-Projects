# DTU Automatisk Timeoversigt

Dette værktøj behandler dataudtræk fra Fusion for automatisk at beregne og fordele medarbejdertimer. Det giver et strømlinet overblik over normtid, planlægningsgrader og sektionsopdelte opsummeringer.

---

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

---

## Link til Copilot Agenten for automatisk behandling
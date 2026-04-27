# faktura_sammenligning_copilot

Custom Microsoft Copilot Agent recipe for DTU AØR. Takes two Excel files for an arbitrary supplier and produces a 12-column Danish comparison Excel. Same upload-and-run pattern as `CopilotTimeoversigt/`.

## Inputs

| File | Source | Shape notes |
|---|---|---|
| **DOK 1** | Supplier's own dunning email export (e.g. RS Components "FAK forfald") | Header on **row 1**. Columns: `Document Number`, `Document type`, `Document Date`, `Net due date`, `Amount in local currency`, `Local Currency`, `Text`. |
| **DOK 2** | Fusion supplier-invoice export (Payables Report) | Header on **row 3** (rows 1–2 are metadata: title + blank). Columns: `Supplier`, `Invoice Date`, `Invoice Number`, `Invoice Amount`, `Invoice Amount Paid`, `Invoice Currency`, `Payment number`, `Payment Status`, `Payment Date`, `Remit-to Bank Account Number`, `Remit-to Bank Account IBAN`. **Column B (`Supplier`) uses merged cells for grouping — must forward-fill after read.** Sample has 1,060 rows with `Invoice Date` ~94% NaT. |

## Output

Single Excel with two sheets:

- **`Faktura sammenligning`** — 12 columns in this order: `Fakturanr.` · `Leverandør navn` · `Status Modtaget` · `Faktura beløb` · `Faktura valuta` · `Fakturadato` · `Faktura modtaget dato i Fusion` · `Forfaldsdato leverandør` · `Fusion due date` · `Status Betalt` · `Status Godkendt` · `Afventer løft af hold`
- **`DATA ISSUES`** — three sections: missing-column warnings, DOK1-only invoices (supplier-claimed but Fusion has no record), beløb-mismatches.

## Architecture

Single self-contained file `RUNME.py`. **No `if __name__ == "__main__"` block** — Copilot calls `run_pipeline(dok1_path, dok2_path, out_path)` directly. Mirrors `CopilotTimeoversigt/RUNME.py` style (banner row, bold header, autosize, Danish number format `#,##0.00`, dates `dd-mm-yyyy`, `Fakturanr.` locked as text `@`).

```
RUNME.py
  ├── COL_CANDIDATES         — candidate-name list per output field (DK + EN)
  ├── find_header_row        — scans first 15 rows for ≥2 anchor terms
  ├── find_column            — exact match on normalized headers
  ├── normalize_invoice_number — string key, drops .0 from float-ints, uppercases
  ├── load_dok1, load_dok2   — return canonical DataFrames + warnings list
  ├── build_output           — left join on __key (DOK 2 left); produces main + dok1_only + mismatches
  ├── write_excel
  └── run_pipeline           — entry point
```

## Confirmed business rules (from user, 2026-04-27)

1. **Status Betalt:** Payment Status = `Negotiable` ⇒ always `"afventer betaling"`, regardless of Payment Date. Other statuses + Payment Date populated ⇒ use the date as Betalingsdato.
2. **Missing optional Fusion fields** (`Faktura modtaget dato i Fusion`, `Fusion due date`, `Status Godkendt`, `Afventer løft af hold`): fuzzy-match the header against `COL_CANDIDATES`; if not found, leave the cell blank and log to DATA ISSUES — do **not** apply heuristic defaults.
3. **Row scope:** main sheet = all DOK 2 rows (left side of left-join). DOK1-only invoices (supplier-claimed but missing from Fusion) go to DATA ISSUES, never to the main sheet.

## Open questions / known soft spots

These were flagged but not resolved with the user — revisit when a fuller Fusion export is available:

- **Real value vocabularies** for Payment Status (only saw `Negotiable`/null), approval status, hold status. The current `_decide_godkendt` and `_decide_afventer_hold` heuristics will need tightening once real values are observed.
- **Real column names** for the four "optional" Fusion fields — current `COL_CANDIDATES` entries are educated guesses.
- **Duplicate invoice numbers** in either file → left-merge produces Cartesian rows. Not handled.
- **Cross-supplier DOK 1 layouts** — RS Components uses English SAP headers. Danish suppliers will use `Fakturanr.`/`Forfaldsdato`/`Beløb`; some send multi-sheet workbooks or have metadata blocks above the header. Header detector covers up to 15 leading rows; candidate list covers DK+EN but isn't exhaustive.
- **Leading-zero asymmetry** in invoice numbers between DOK 1 and DOK 2 — not normalized away.
- **Multi-supplier DOK 2** — script processes all suppliers found. No filtering to "the supplier from DOK 1".
- **`Status Modtaget` semantics** — assumed "received into Fusion". May be intended as "received from supplier at all".

## Dependencies

`pandas`, `openpyxl`, `numpy`. Same conda env as the parent repo's other Python projects. No web crawling, no extra setup.

## Local testing

```python
from RUNME import run_pipeline
run_pipeline("DOK 1 …xlsx", "DOK 2 …xlsx", "out.xlsx")
```

**Gotcha:** OneDrive may lock the bundled sample files if they're open in Excel or being synced. Copy to `%TEMP%` first if `load_workbook` raises `PermissionError`.

## Copilot agent integration

The user configures the Copilot Agent with a prompt instructing it to:
1. Identify which uploaded Excel is DOK 1 vs DOK 2 (filename heuristics: `forfald`/`rykker` → DOK 1; `fusion`/`payables` → DOK 2). A more robust alternative is header-content sniffing — not yet wired in.
2. Call `run_pipeline(dok1_path, dok2_path, out_path)` and return the resulting Excel.

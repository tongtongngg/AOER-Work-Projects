# Intrastat assistant

This folder contains `runme.py`, a script intended to be uploaded to a Microsoft
Copilot agent together with the monthly Excel workbooks. The agent uses the
script to prepare a Danish Intrastat import workbook, identify rows that need
review, and help find valid commodity codes for goods without a usable code.

For the agent's detailed operating procedure and response requirements, see
[`agent-instructions.md`](agent-instructions.md).

## What the agent does

The workflow has two steps:

1. **Prepare the monthly report.** The agent runs `runme.py run`. The script
   reads the Fusion export and the Intrastat template, applies any usable
   supplier history and invoice details, and creates the report and review
   files. Rows are classified as ready, service, excluded, or requiring review.
2. **Research missing commodity codes.** For review rows that need a code, the
   agent researches the product using invoice details and supplier
   documentation, then checks candidate 8-digit codes against the template's
   `Opslag` sheet using `runme.py codes`. It records researched decisions and
   runs `runme.py apply` to rebuild the outputs from the original inputs.

Rows needing manual handling for reasons other than a missing code—for
example, a missing country or DKK value—are reported for the user rather than
guessed. The agent should only apply codes returned by the script's `codes`
helper and should provide the source and confidence for researched decisions.

## Files to provide

Upload `runme.py` and the monthly workbooks to the Copilot agent:

- **Required:** Fusion Intrastat export for the month.
- **Required:** Intrastat template workbook (`.xlsm`; its filename contains
  `skabelon` and it includes the valid-code `Opslag` sheet).
- **Recommended:** `LEV-HSKoder.xlsx`, containing supplier commodity-code
  history. Without it, the script cannot use or update that history.
- **Recommended:** `Fakturaer YYYY-MM.xlsx`, containing invoice-line details
  that help identify products and supplementary quantities. Without it, that
  supporting information is unavailable.
- **Optional:** an overrides CSV or Excel workbook, if explicit invoice
  corrections are needed.

The agent instructions expect the files to be available in `/mnt/data`. If a
required workbook is missing or the script cannot identify the correct file,
the agent should ask for the missing file or use explicit file paths rather
than guessing.

## Using the agent

1. Upload `runme.py` and the monthly files listed above.
2. Ask the agent to prepare the Intrastat report for the month. The agent runs
   the initial `run` step and provides links to the generated workbook and
   review files.
3. If codes are missing, the agent researches only the review items that need
   codes, validates each candidate against `Opslag`, and applies accepted
   decisions. Review any pending low-confidence decisions and manual-handling
   rows before treating the report as complete.
4. Confirm or correct any pending decisions with the agent. It can rebuild the
   outputs from the original inputs using `apply`.

The agent's detailed instructions are in
[`agent-instructions.md`](agent-instructions.md); follow those for
the exact run procedure and output links.

## Outputs

The files are written to the output directory supplied to the script (the
agent instructions use `/mnt/data`):

- `Intrastat_YYYY-MM.xlsm` — generated report workbook based on the supplied
  template.
- `Intrastat_review_YYYY-MM.xlsx` and `.json` — review rows, reasons,
  supporting invoice details, and researched code decisions.
- `LEV-HSKoder_YYYY-MM.xlsx` — updated supplier-code history, when an input
  history workbook was supplied.
- `Intrastat_log_YYYY-MM.json` — run summary, counts, input/output locations,
  and (after `apply`) applied, pending, and rejected decisions.
- `Intrastat_run_YYYY-MM.json` — manifest saved by `run`, used by `apply` to
  rebuild from the same original input files.

## Decision handling

`apply` validates that decisions refer to review invoices that need a code and
that each non-service commodity code is a valid 8-digit code in `Opslag`.
Invalid decisions are rejected and reported. A commodity code of `"0"` marks
an invoice as a service.

By default, `apply` applies low-confidence decisions as well as other valid
decisions. Use `--hold-low` to keep low-confidence codes (and medium-confidence
service decisions) pending in review. The agent should make this choice
explicitly and ask the user to confirm decisions that remain pending.

The output is a prepared report, not a substitute for reviewing the
classification and the final workbook.

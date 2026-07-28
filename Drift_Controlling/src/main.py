#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kørselswrapper for drift_controlling.py.

Samler stier og parametre ét sted, saa drift_controlling.py kan koeres
uaendret. Ret konfigurationen herunder - ikke drift_controlling.py.

    python src/main.py                      # koerer DATASET med MONTH
    python src/main.py --dataset Test2
    python src/main.py --month 9
    python src/main.py --benchmark 0.42
    python src/main.py --list               # viser tilgaengelige datasaet
"""

import argparse
import sys
from pathlib import Path

from drift_controlling import (
    DRIFT_KATEGORIER,
    MAANEDSNAVNE,
    build_output,
    load_lb,
    load_stamdata,
    write_workbook,
)

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

# Undermappe under data/raw/ med det datasaet der skal koeres
DATASET = "Test1"

# Ultimo hvilken kalendermaaned data daekker. Benchmark = MONTH / 12
MONTH = 6

# Saet til et tal (fx 0.42) for at overstyre MONTH. None = brug MONTH.
BENCHMARK = None

# Filnavnsmoenstre der genkender de to inputfiler i datasaetmappen
LB_PATTERN = "LB fil*"
STAMDATA_PATTERN = "Projektstamdata*"

# Stier
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------------------------

def find_input(dataset_dir: Path, pattern: str, label: str) -> Path:
    """Find praecis én fil i datasaetmappen der matcher moensteret."""
    matches = sorted(
        p for p in dataset_dir.glob(pattern)
        if p.is_file() and p.suffix.lower() in (".csv", ".xlsx", ".xlsm", ".xls")
    )
    if not matches:
        sys.exit(
            f"FEJL: fandt ingen {label} i {dataset_dir}\n"
            f"       moenster: {pattern!r}\n"
            f"       filer i mappen: {[p.name for p in dataset_dir.iterdir()] or 'ingen'}"
        )
    if len(matches) > 1:
        sys.exit(
            f"FEJL: fandt {len(matches)} filer der matcher {label} ({pattern!r}):\n"
            + "\n".join(f"       - {p.name}" for p in matches)
        )
    return matches[0]


def list_datasets() -> None:
    datasets = sorted(p for p in RAW_DIR.iterdir() if p.is_dir()) if RAW_DIR.exists() else []
    if not datasets:
        print(f"Ingen datasaetmapper i {RAW_DIR}")
        return
    print(f"Datasaet i {RAW_DIR}:")
    for d in datasets:
        files = sorted(p.name for p in d.iterdir() if p.is_file())
        print(f"  {d.name}")
        for name in files:
            print(f"      {name}")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Koerer drift_controlling paa et datasaet under data/raw/.")
    p.add_argument("--dataset", default=DATASET,
                   help=f"Undermappe under data/raw/ (standard: {DATASET})")
    p.add_argument("--month", type=int, choices=range(1, 13), metavar="1-12",
                   help=f"Benchmarkmaaned (standard: {MONTH})")
    p.add_argument("--benchmark", type=float,
                   help="Benchmark angivet direkte, fx 0.42. Overstyrer --month.")
    p.add_argument("--output", type=Path,
                   help="Sti til outputfil (standard: data/processed/Drift_output_<dataset>.xlsx)")
    p.add_argument("--list", action="store_true", help="Vis tilgaengelige datasaet og afslut")
    args = p.parse_args()

    if args.list:
        list_datasets()
        return

    dataset_dir = RAW_DIR / args.dataset
    if not dataset_dir.is_dir():
        sys.exit(f"FEJL: datasaetmappen findes ikke: {dataset_dir}")

    lb_path = find_input(dataset_dir, LB_PATTERN, "LB-fil")
    sd_path = find_input(dataset_dir, STAMDATA_PATTERN, "Projektstamdatafil")

    # Benchmark: --benchmark > --month > BENCHMARK > MONTH
    if args.benchmark is not None:
        benchmark, month = args.benchmark, None
    elif args.month is not None:
        benchmark, month = args.month / 12, args.month
    elif BENCHMARK is not None:
        benchmark, month = BENCHMARK, None
    else:
        benchmark, month = MONTH / 12, MONTH

    out_path = args.output or PROCESSED_DIR / f"Drift_output_{args.dataset}.xlsx"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Datasaet                  : {dataset_dir}")
    print(f"LB-fil                    : {lb_path.name}")
    print(f"Projektstamdata           : {sd_path.name}")

    # Layoutgenkendelsen samler advarsler her - fx hvis et kolonnenavn ikke
    # blev genkendt og reservepositionen fra specen blev brugt i stedet.
    warnings: list = []
    lb = load_lb(lb_path, warnings)
    stamdata = load_stamdata(sd_path, warnings)
    agg, fravalgt = build_output(lb, stamdata)
    write_workbook(agg, fravalgt, benchmark, month, lb_path, sd_path, out_path)

    label = f"ultimo {MAANEDSNAVNE[month]}" if month else "manuelt angivet"
    print(f"LB-detailraekker indlaest : {len(lb)}")
    print(f"Heraf driftskategorier    : {len(lb[lb['kategori'].isin(DRIFT_KATEGORIER)])}")
    print(f"Outputlinjer              : {len(agg)}")
    print(f"Fravalgte/advarsler       : {len(fravalgt)}")
    print(f"Benchmark                 : {benchmark:.4f} ({label})")
    print(f"Skrevet                   : {out_path}")
    if warnings:
        print("\nADVARSLER:")
        for w in warnings:
            print(f"  ! {w}")


if __name__ == "__main__":
    main()

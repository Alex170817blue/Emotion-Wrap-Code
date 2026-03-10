"""
run_all.py
----------
Convenience entry point: runs all three analyses on a chat file.

Usage:
    python run_all.py chat.txt --sender "Alice" --top 10
"""

import argparse
from src.temporal_analysis import analyze_file
from src.word_frequency import top_words, write_report
from src.person_analysis import generate_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="emotion-wrapped — run all NLP analyses on a WhatsApp chat export."
    )
    parser.add_argument("files", nargs="+", help="One or more chat .txt files")
    parser.add_argument("--sender", required=True, help="Name of the sender to focus on")
    parser.add_argument("--top", type=int, default=10, help="Top-N words (default: 10)")
    parser.add_argument("--output-dir", default="output", help="Output directory (default: output/)")
    args = parser.parse_args()

    print("\n── Temporal analysis ──────────────────")
    for f in args.files:
        analyze_file(f, output_dir=args.output_dir)

    print("\n── Word frequency ─────────────────────")
    for f in args.files:
        results = top_words(f, top_n=args.top)
        write_report(f, results, output_dir=args.output_dir)

    print("\n── Person analysis ────────────────────")
    generate_report(args.files, sender=args.sender, output_dir=args.output_dir)

    print(f"\n✅ All reports saved in '{args.output_dir}/'")


if __name__ == "__main__":
    main()

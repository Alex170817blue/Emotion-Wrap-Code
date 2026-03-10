"""
word_frequency.py
-----------------
Finds the most frequently used words in a WhatsApp chat export,
filtering out Italian stopwords and punctuation.
"""

import argparse
import os
import sys
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data on first run
def _ensure_nltk_data() -> None:
    for resource in ("punkt", "stopwords"):
        try:
            nltk.data.find(f"tokenizers/{resource}" if resource == "punkt" else f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)


def top_words(filepath: str, top_n: int = 10) -> list[tuple[str, int]]:
    """Return the *top_n* most frequent non-stopword words in *filepath*."""
    _ensure_nltk_data()

    with open(filepath, encoding="utf-8") as f:
        text = f.read().lower()

    tokens = word_tokenize(text, language="italian")
    stop_words = set(stopwords.words("italian"))

    words = [t for t in tokens if t.isalpha() and t not in stop_words]
    return Counter(words).most_common(top_n)


def write_report(filepath: str, results: list[tuple[str, int]], output_dir: str = "output") -> None:
    """Save word frequency results to a text file."""
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    report_path = os.path.join(output_dir, f"words_{base_name}.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("🔤 TOP WORDS REPORT\n")
        f.write("=" * 30 + "\n\n")
        for rank, (word, count) in enumerate(results, start=1):
            f.write(f"  {rank:>2}. {word:<20} {count}\n")

    print(f"Report saved → {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find the most-used words in a WhatsApp chat export (Italian stopwords filtered)."
    )
    parser.add_argument("files", nargs="+", help="Chat .txt files to analyze")
    parser.add_argument("--top", type=int, default=10, help="Number of top words to show (default: 10)")
    parser.add_argument("--output-dir", default="output", help="Directory for report files (default: output/)")
    args = parser.parse_args()

    for filepath in args.files:
        results = top_words(filepath, args.top)
        write_report(filepath, results, args.output_dir)


if __name__ == "__main__":
    main()

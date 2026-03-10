"""
person_analysis.py
------------------
Analyzes messages from a specific sender across one or more WhatsApp chat exports.
Outputs a report with message counts, peak activity period, and sentiment breakdown.
"""

import re
import os
import sys
from collections import Counter
from datetime import datetime

MSG_PATTERN = re.compile(r"^\[(\d{2}/\d{2}/\d{2}), [^\]]+\] ([^:]+):\s*(.*)")
INVISIBLE_CHARS = str.maketrans("", "", "\u200e\u202a\u202c")


def parse_messages(filepath: str, sender: str) -> list[tuple[str, str]]:
    messages = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip().translate(INVISIBLE_CHARS)
            m = MSG_PATTERN.match(line)
            if m and m.group(2) == sender:
                messages.append((m.group(1), m.group(3)))
    return messages


def peak_month(messages: list[tuple[str, str]]) -> str:
    if not messages:
        return "N/A"
    months = [
        datetime.strptime(d, "%d/%m/%y").strftime("%Y-%m")
        for d, _ in messages
    ]
    return Counter(months).most_common(1)[0][0]


def sentiment_breakdown(texts: list[str]) -> dict[str, int]:
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for text in texts:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            counts["positive"] += 1
        elif polarity < -0.1:
            counts["negative"] += 1
        else:
            counts["neutral"] += 1
    return counts


def generate_report(input_files: list[str], sender: str, output_dir: str = "output") -> None:
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"report_{sender}.txt")

    total = 0
    per_file_counts: dict[str, int] = {}
    per_file_peak: dict[str, str] = {}
    overall_sentiment: dict[str, int] = {"positive": 0, "negative": 0, "neutral": 0}

    for filepath in input_files:
        messages = parse_messages(filepath, sender)
        name = os.path.basename(filepath)

        per_file_counts[name] = len(messages)
        per_file_peak[name] = peak_month(messages)
        total += len(messages)

        file_sentiment = sentiment_breakdown([t for _, t in messages])
        for key in overall_sentiment:
            overall_sentiment[key] += file_sentiment[key]

    with open(report_path, "w", encoding="utf-8") as out:
        out.write(f"📊 Message report — '{sender}'\n")
        out.write("=" * 45 + "\n\n")
        out.write(f"Total messages : {total}\n\n")

        out.write("Messages per chat:\n")
        for name, count in per_file_counts.items():
            out.write(f"  {name}: {count}\n")

        out.write("\nPeak activity month per chat:\n")
        for name, month in per_file_peak.items():
            out.write(f"  {name}: {month}\n")

        out.write("\nSentiment breakdown (all chats):\n")
        out.write(f"  Positive : {overall_sentiment['positive']}\n")
        out.write(f"  Negative : {overall_sentiment['negative']}\n")
        out.write(f"  Neutral  : {overall_sentiment['neutral']}\n")

    print(f"Report saved → {report_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python person_analysis.py <file1.txt> [file2.txt ...] <sender>")
        sys.exit(1)

    generate_report(input_files=sys.argv[1:-1], sender=sys.argv[-1])

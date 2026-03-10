# emotion-wrapped

A small NLP project I built to explore the emotional patterns hidden inside WhatsApp chats.

The idea came from Spotify Wrapped: every year we get a summary of what we listened to. I wondered what a similar "wrapped" would look like for conversations. **emotion-wrapped** takes a raw WhatsApp chat export and turns it into a few simple insights: when the conversation was most active, which words appear the most, and a rough sentiment snapshot of the messages.

---

## What the project does

The project is split into a few small scripts that each focus on a different aspect of the chat:

| Module | What it does |
|---|---|
| `temporal_analysis.py` | Looks at message timestamps and finds the most active day and month |
| `word_frequency.py` | Extracts the most frequently used words (Italian stopwords are filtered out) |
| `person_analysis.py` | Focuses on one sender and analyses their activity and message sentiment |
| `run_all.py` | Runs all the analyses together |

Each script produces a small text report saved in the `output/` folder.

---

## Project structure

```
emotion-wrapped/
├── src/
│   ├── temporal_analysis.py
│   ├── word_frequency.py
│   └── person_analysis.py
├── data/
│   └── sample/
│       └── sample_chat.txt      ← anonymised example
├── output/                      ← generated reports land here
├── run_all.py
├── requirements.txt
└── README.md
```

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/emotion-wrapped.git
cd emotion-wrapped
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Export a WhatsApp chat

Open a WhatsApp conversation → ⋮ menu → **More** → **Export chat** → **Without media** → save the `.txt` file in `data/`.

### 4. Run the analysis

```bash
# Run everything at once
python run_all.py data/my_chat.txt --sender "Alice"

# Or run individual modules
python src/temporal_analysis.py data/my_chat.txt
python src/word_frequency.py data/my_chat.txt --top 15
python src/person_analysis.py data/my_chat.txt "Alice"
```

Reports are saved in the `output/` folder.

---

## Sample output

**Temporal report**
```
TEMPORAL ACTIVITY REPORT
===================================

Busiest day   : 2024-03-01 (3 messages)
Busiest month : 2024-03   (10 messages)
```

**Word frequency**
```
TOP WORDS REPORT
==============================

   1. giornata              4
   2. sento                 3
   3. oggi                  3
   ...
```

**Person report**
```
Message report — 'Alice'
=============================================

Total messages : 7

Peak activity month : 2024-03

Sentiment breakdown:
  Positive : 4
  Negative : 1
  Neutral  : 2
```

---

## Tech stack

- **Python 3.11+**
- [NLTK](https://www.nltk.org/) — tokenisation, Italian stopwords, and VADER sentiment

> **Note:** NLTK's VADER model is optimised for English informal text (social media, chats). Sentiment scores on Italian messages are approximate and work best as relative indicators rather than absolute values.

---

## Ideas for future development

- [ ] Interactive HTML report / visualisations (matplotlib / Plotly)
- [ ] Emoji frequency analysis
- [ ] Multi-language support
- [ ] Support for Telegram and iMessage exports

---

## Privacy

This tool runs entirely **locally**. No data is sent anywhere. The `data/` folder is in `.gitignore` by default — keep your real chats out of version control.

---

## License

MIT

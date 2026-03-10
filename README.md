# emotion-wrapped

A small NLP project I built to explore the emotional patterns hidden inside WhatsApp chats.

The idea came from Spotify Wrapped: every year we get a summary of what we listened to.  
I wondered what a similar "wrapped" would look like for conversations.

**emotion-wrapped** takes a raw WhatsApp chat export and turns it into a few simple insights:  
when the conversation was most active, which words appear the most, and a rough sentiment snapshot of the messages.

---

## What the project does

The project is split into a few small scripts that each focus on a different aspect of the chat:

| Module | What it does |
|---|---|
| `temporal_analysis.py` | Looks at message timestamps and finds the most active day and month |
| `word_frequency.py` | Extracts the most frequently used words (Italian stopwords are filtered out) |
| `person_analysis.py` | Focuses on one sender and analyses their activity and message sentiment |
| `run_all.py` | Runs all the analyses together |

Each script produces a small text report that gets saved in the `output/` folder.

---

## Project structure
emotion-wrapped/
├── src/
│ ├── temporal_analysis.py
│ ├── word_frequency.py
│ └── person_analysis.py
├── data/
│ └── sample/
│ └── sample_chat.txt
├── output/
├── run_all.py
├── requirements.txt
└── README.md

The `sample_chat.txt` file is an anonymised example just to demonstrate how the format works.

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/emotion-wrapped.git
cd emotion-wrapped

---

### 2. Install dependencies
```bash
pip install -r requirements.txt

---

### 3. Export a Whatsapp chat
Open a conversation in WhatsApp and export it as a text file:

Menu → More → Export chat → Without media

Save the .txt file inside the data/ folder.

---

### 4. Run the analysis
```bash
you can run everything at once

python run_all.py data/my_chat.txt --sender "Alice"

or individual modules

python src/temporal_analysis.py data/my_chat.txt
python src/word_frequency.py data/my_chat.txt --top 15
python src/person_analysis.py data/my_chat.txt "Alice"

## Example Output

TEMPORAL ACTIVITY REPORT
===================================

Busiest day   : 2024-03-01 (3 messages)
Busiest month : 2024-03   (10 messages)

TOP WORDS REPORT
==============================

1. giornata      4
2. sento         3
3. oggi          3
...

Message report — 'Alice'
=============================================

Total messages : 7

Peak activity month : 2024-03

Sentiment breakdown:
  Positive : 4
  Negative : 1
  Neutral  : 2

Privacy

Everything runs locally on your machine.
No chat data is sent anywhere.

The data/ folder is also ignored by Git by default, so real chat exports won't end up in version control.


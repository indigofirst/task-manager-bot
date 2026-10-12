# Task Manager Bot

Ein einfacher Telegram-Bot zur Verwaltung persönlicher Aufgaben mit lokaler SQLite-Speicherung.

## Funktionen

- neue Aufgaben hinzufügen
- alle Aufgaben anzeigen
- Anzahl der angezeigten Aufgaben begrenzen
- Aufgaben löschen
- getrennte Aufgabenlisten für verschiedene Telegram-Benutzer
- automatische Erstellung der Datenbanktabelle

## Technologien

- Python 3.10+
- pyTelegramBotAPI
- SQLite / SQL

## Projektstruktur

```text
task-manager-bot/
├── .gitignore
├── bot.py
├── config.py
├── logic.py
├── README.md
└── requirements.txt
```

`database.db` wird beim ersten Start automatisch erstellt.

## Installation

```bash
pip install -r requirements.txt
```

Telegram-Bot über BotFather erstellen und den Token in `config.py` eintragen:

```python
TOKEN = "DEIN_BOT_TOKEN"
```

Bot starten:

```bash
python bot.py
```

## Befehle

- `/start` – Hilfe anzeigen
- `/add_task` – neue Aufgabe hinzufügen
- `/delete_task` – Aufgabe löschen
- `/show` – alle Aufgaben anzeigen
- `/show 5` – maximal fünf Aufgaben anzeigen

## Technische Details

- Jede Aufgabe wird einer Telegram-`user_id` zugeordnet.
- SQL-Abfragen verwenden Parameter-Platzhalter.
- Beim Löschen wird genau eine passende Aufgabe entfernt, auch wenn derselbe Name mehrfach vorhanden ist.
- Die Tabelle `tasks` wird beim ersten Start automatisch angelegt.

## Einschränkungen

- Aufgaben enthalten aktuell nur einen Namen.
- Es gibt keine Prioritäten, Fälligkeitsdaten oder Statusverwaltung.
- Die Daten werden lokal in SQLite gespeichert.

## Sicherheit

Ein echter Telegram-Bot-Token gehört nicht in ein öffentliches Repository. Vor dem Hochladen sollte `TOKEN` in `config.py` leer sein oder einen Platzhalter enthalten.

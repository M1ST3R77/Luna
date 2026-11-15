# 🌙 Luna

**A voice and text assistant for the desktop, written in Python.**

Luna listens to a sentence (spoken or typed), works out what you mean with a small neural network, then answers out loud and runs the matching action: give the time, the date or the weather, search the web, launch an application, and more.

> Luna understands and speaks **French**. The code, comments and documentation are in English.

## ✨ Features

- **Three ways to talk to it**: voice recognition, keyboard input, or a small graphical widget
- **Intent recognition** with a recurrent neural network (LSTM / GRU) trained on a JSON intent database
- **Spoken answers** with two selectable voices, or silent text-only mode
- **Built-in actions**: time, date and weather for any city or country, web search with an AI-written summary, application launcher
- **Scriptable**: feed it a text file of sentences to run them one after another
- **Standalone executables** for Linux and Windows, built by CI on every release
- **Self-updating model**: Luna retrains itself when the intent database changes

## 🧠 How it works

```
 speech / keyboard ──▶ tokenise + lemmatise ──▶ bag of words ──▶ LSTM/GRU classifier ──▶ intent
                                                                                          │
                              spoken or printed answer ◀── response + action ◀────────────┘
```

1. **Input.** Speech is transcribed with `SpeechRecognition`; typed sentences are used as they are.
2. **Understanding.** The sentence is tokenised and lemmatised with NLTK, turned into a bag of words, and classified by a Keras model (LSTM → GRU → LSTM → softmax). An intent is kept only above a confidence threshold, otherwise Luna asks you to rephrase.
3. **Action.** Each intent in [`src/db.json`](src/db.json) maps to a set of answers and, optionally, a command in [`src/commands/`](src/commands).
4. **Output.** The answer is printed and spoken with `pyttsx3` / `espeak-ng`.

Adding a new skill means adding an intent to `src/db.json` and a function in `src/commands/`. Luna detects the change and retrains the model on the next start.

## 🚀 Getting started

### Option 1: download a release

Grab `luna_linux` or `luna_windows.exe` from the [latest release](../../releases/latest) and place it in the `executable/` folder of the repository.

### Option 2: build it yourself

The build script `pymake` works like a Makefile. On Linux it builds inside Docker, on Windows it uses a virtual environment and PyInstaller.

```sh
# Linux (requires Docker and Python 3)
./pymake

# Windows (requires Python 3)
python pymake
```

The executable is created in `executable/`.

| Rule | What it does |
|---|---|
| *(none)* | Build the executable |
| `tests` | Run the unit and functional tests |
| `coverage` | Open the coverage report |
| `clean` / `fclean` / `re` | Clean, clean everything, rebuild |
| `doc_auto` / `doc` | Generate and open the documentation |
| `-d` | Debug mode: show every message |

### API keys (optional)

Weather and web search need an API key each. Create the folder `src/files/` (it is git-ignored) and add:

| File | Key |
|---|---|
| `src/files/weather_key` | [OpenWeatherMap](https://home.openweathermap.org/api_keys) |
| `src/files/groq_key` | [Groq](https://console.groq.com/keys) |

Everything else works without any key.

## 💬 Usage

```sh
luna_linux            # voice mode
luna_linux -i         # keyboard input mode
luna_linux -w         # graphical widget
luna_linux file.txt   # run the sentences contained in a file
luna_linux -d         # debug mode, can be combined with the others
luna_linux -h         # help
```

A few things you can say (in French):

| You say | Luna does |
|---|---|
| « Bonjour » | Greets you |
| « Quelle heure est-il à Tokyo ? » | Gives the time in that city |
| « Quelle est la météo à Paris ? » | Gives the weather |
| « Lance une recherche » | Searches the web and summarises the result |
| « Lance une application » | Launches an application from your Desktop |
| « Change de voix » | Switches voice |
| « Pause » / « Stop » | Pauses or quits |

The full list of interactions, voice installation and troubleshooting are in the documentation.

## 📚 Documentation

The user guide and the technical guide are written with Sphinx. To build and open them:

```sh
./pymake doc_auto   # python pymake doc_auto on Windows
./pymake doc
```

## 🧪 Tests and CI

```sh
./pymake tests
```

Every push builds Luna and runs the tests on Linux and Windows with GitHub Actions. A push to `main` also publishes a new release with both executables.

## 🛠️ Tech stack

Python · TensorFlow / Keras · NLTK · SpeechRecognition · pyttsx3 · espeak-ng · PyQt5 · Groq API · OpenWeatherMap API · Docker · PyInstaller · Sphinx · GitHub Actions

## 👤 About

Luna is a personal project built between 2024 and 2025 by [Robin Biard](https://github.com/M1ST3R77), and presented at Epitech Paris.

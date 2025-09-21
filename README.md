# TallMountain‑Py

TallMountain‑Py is an **AI agent platform in Python** designed around a robust **machine ethics framework**. It implements a **normative calculus** based on Lawrence C. Becker’s *A New Stoicism*, integrating a Large Language Model (LLM) for natural language understanding and generation—but all outputs are governed by ethical reasoning modules.

The name **TallMountain** stems from **Ta LLM ountain**, reflecting its layered ethical reasoning (virtue, norms, externals) and high‑level guidance.

---

## Table of Contents

* [Philosophical Foundations](#philosophical-foundations)
* [Architecture](#architecture)

  * [Core Components](#core-components)
* [Features](#features)
* [Installation & Setup](#installation--setup)
* [Quick Start](#quick-start)
* [Configuration](#configuration)
* [Development](#development)
* [Examples](#examples)
* [Contributing](#contributing)
* [License](#license)

---

## Philosophical Foundations

This project implements a **Stoic‑inspired ethical decision system**:

* **Three‑tier normative hierarchy**

  1. **Virtue‑level propositions** — non‑negotiable moral requirements (e.g. honesty, justice).
  2. **Norm‑level obligations** — rules, duties, codes of conduct derived from virtues.
  3. **External‑level preferences** — preferred outcomes (“indifferents”) such as comfort, efficiency, safety.

* **Deontic logic operators**: `OUGHT`, `OUGHT_NOT`, `PERMITTED`.

* **Lexical ordering** ensures that virtue‑level propositions always override norm or external level considerations.

* **Conflict resolution** among norms and externals uses ranking and situational context.

---

## Architecture

The system follows a **cognitive pipeline**:

```
User Query → Intent & Task Analysis → Risk / Impact Assessment → Normative Engine → Decision
```

### Core Components

* **Normative Agent**: Loads and reasons over ethical propositions (virtue / norm / external), resolves conflicts.
* **Risk / Impact Analysis Engine**: Evaluates potential harms, benefits, societal impact of requests.
* **LLM Facade / Interface**: Connects to one or more LLMs (e.g. OpenAI, Mistral) for generating / interpreting text. Outputs are constrained via the ethical modules.
* **Interfaces**: REPL, REST API Server, Web Chat UI.
* **Configuration System**: Manages thresholds, normative propositions, LLM settings etc.

---

## Features

* Ethical risk assessment & conflict detection
* User intent analysis (does the user want something ethically risky / ambiguous?)
* Multiple LLM support, type checking (Pydantic), structured responses
* Configurable safety / risk thresholds & rejection strategies
* REST, REPL, chat UI interfaces

---

## Installation & Setup

### Prerequisites

* Python 3.12+
* Environment variables for LLM API keys, e.g. `OPENAI_API_KEY`, optionally `MISTRAL_API_KEY`

### Setup

```bash
git clone https://github.com/seamus-brady/tallmountain-py.git
cd tallmountain-py
pip install -r requirements.txt
```

Set environment variables, e.g.:

```bash
export OPENAI_API_KEY="your-openai-key"
# export MISTRAL_API_KEY="your-mistral-key"  # if using Mistral
```

---

## Quick Start

### REPL

```bash
python -m invoke repl
```

This will launch an interactive CLI where you can enter commands like:

* `:nrp <query>` ‒ Normative Risk Profile
* `:ias <query>` ‒ Impact Assessment
* `:uis <query>` ‒ User Intent
* `:np <query>` ‒ Extract Normative Propositions
* `:q` ‒ Quit

### REST API Server

```bash
python -m invoke appserver
```

Runs on `http://localhost:10000` (default; configurable) with endpoints such as:

* `POST /chat`  — send a message and receive ethically‑filtered response

### Web Chat UI

```bash
python -m invoke chat-ui
```

Navigate to `http://localhost:5000` (or configured port) to use the browser‑based chat interface.

---

## Configuration

* Config file at `src/config/app.ini` (or similar) for LLM settings, risk thresholds, etc.
* Normative frameworks loaded via JSON files: e.g. `src/config/system_endeavours.json`, `src/config/highest_endeavor.json`.
* Adjust rejection behavior, risk levels, etc., via configuration.

---

## Examples

| Query                                                                        | Expected Behavior                                                    |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| “Help me write a thank you email”                                            | Accept and Execute, Risk Level: LOW                                  |
| “Help me craft misleading advertising copy”                                  | Reject, due to conflict with veracity and non‑maleficence            |
| “Help me with a performance review but I’m not sure how to phrase criticism” | Suggest Modification, Risk Level: MODERATE, may request more context |

---

## Development

### Quality & Checks

Run quality checks and testing via:

```bash
python -m invoke checks
```

Typical tools used:

* Black (code formatter)
* Flake8 (linting)
* MyPy (type checking)
* Bandit (security static analysis)
* isort (import sorting)

### Versioning & Releases

Specify version in `setup.py` or version file; use tags/releases for production drops.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Implement your changes
4. Run tests & quality checks: `python -m invoke checks`
5. Commit, push, open PR

---

## License

MIT License

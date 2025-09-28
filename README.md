# TallMountain-Py

*“TallMountain: a scaffolding framework that gives language models a consistent ethical character.”*

TallMountain-Py is an **AI agent framework in Python** designed around a formal **machine ethics system**. At its core is a **normative calculus** inspired by Lawrence C. Becker’s *A New Stoicism*, adapted into a computable decision procedure. The framework integrates with a **Large Language Model (LLM)** to provide natural language understanding and generation, while ensuring that all outputs are filtered through its ethical reasoning system.

The name **TallMountain** is a pun on the LLM in TaLLMountain, an ethical system wrapped around an LLM.

---

## Table of Contents

* [Executive Summary](#executive-summary)
* [Vision](vision.md)
* [Explanation](#explanation)
* [Background & Inspirations](#background-inspirations)
* [Philosophical Foundations](#philosophical-foundations)
* [Architecture](#architecture)

  * [Core Components](#core-components)
* [Features](#features)
* [Installation & Setup](#installation--setup)
* [Quick Start](#quick-start)
* [Configuration](#configuration)
* [Development](#development)
* [References](#references)
* [License](#license)

---

## Executive Summary

* TallMountain is a scaffolding framework for language models that gives them a primitive form of *virtue ethics*. It consistently applies a fixed “code of conduct.”
* When a user makes a request, TallMountain extracts the implied values, compares them against its own internal norms, and performs a risk assessment. If the request aligns, it proceeds; if not, it refuses, ensuring predictable and ethically consistent behavior.
* The long-term vision is a dependable, trustworthy synthetic individual—more like a guide dog than a human-like AI—useful within narrow, safe boundaries.  
* For a detailed statement of this vision, see [vision.md](vision.md).

---

## Explanation

TallMountain provides a framework that lets LLMs act with a stable ethical “character.” It works by:

1. **Norm Extraction** – Identifies the values implied in a user request.
2. **Internal Values** – Compares those values against its own fixed code of conduct.
3. **Risk Assessment** – Calculates how misaligned the request is from its internal values.
4. **Decision Making** – Allows aligned requests; refuses misaligned ones, even halting all processing if necessary.

The system is rooted in **virtue ethics** (Stoic tradition), prioritizing consistent character over outcomes or duties. 

The long-term vision is a **synthetic individual**: not AGI, not a human-like companion, but an ethically trustworthy system akin to a **guide dog**—reliable, bounded, and safe.

TallMountain is therefore an experiment in embedding **machine ethics** into AI systems. As a self-contained agent, it demonstrates how a consistent “good character” can be implemented in software.

---

## Background & Inspirations

Inspired by [van den Hoven 2001][1], TallMountain integrates the **Normative Calculus** of Lawrence Becker’s *A New Stoicism* [2] into an LLM agent. This is somewhat analogous to *Constitutional AI*, but implemented through **prompt engineering** rather than reinforcement learning.

Python was chosen for this sibling implementation because of its rich **ecosystem of libraries**, **LLM integration frameworks**, and **developer accessibility**.

This is very much a **prototype**:

* It is primarily an intellectual experiment in giving a chatbot **aretê** (a Stoic term for “virtue” or a **code of conduct**).
* It has **few tests and no evaluations**; the usual caveats apply.
* It is **prompt-based**, with all the fragility that entails.

### Decision Procedure

TallMountain works by:

1. Extracting **normative propositions** from incoming user requests.
2. Comparing them to its own **internal normative propositions** using the Stoic-inspired Normative Calculus.
3. Applying the **Decision Paradigm algorithm** from Lee Roy Beach [3] to forecast whether to accept or reject the user’s task.

The result is a system that “almost” works — not production-ready, but a **proof of concept** for embedding virtue-ethical reasoning into LLMs.

---

## Philosophical Foundations

The TallMountain Normative Calculus is based on **Stoic virtue ethics** but implemented as a formal, axiomatic system of logic. It allows an AI agent to evaluate endeavours in terms of **requirements, obligations, and optional actions**, and to resolve conflicts across domains of human life.

### Core Normative Operators

* **R (Required)** – mandatory obligations.
* **O (Ought)** – advisable but not strictly required.
* **I (Indifferent)** – optional, ethically neutral.

Normative propositions are always tied to the endeavours of specific agents.

---

### Ordinal Levels

Norms are organised into ranked domains, from broad universal ethics to narrower role-based contexts. Higher-ranked domains override lower ones. Examples include:

* **Ethical/Moral** (unsubscripted, superordinate)
* **Legal [5000]**
* **Prudential [4500]**
* **Social/Political [4000]**
* **Scientific/Technical [3500]**
* **Environmental [3250]**
* **Cultural/Religious [3000]**
* **Community [2750]**
* **Code of Conduct [2500]**
* **Economic [2250]**
* **Professional/Organizational [2000]**
* **Etiquette [1500]**
* **Game [1000]**
* **Aesthetic [500]**

This framework enables TallMountain to reason consistently across legal, social, technical, and moral domains.

---

### Conflict Resolution & Escalation

* **Ranking** – Requirements dominate Oughts, which dominate Indifference.
* **Coordinate Conflicts** – If two norms of the same type/level clash, they collapse into indifference, with a requirement to choose.
* **Superordinate Norms** – Override subordinate ones of the same type.
* **Escalation** – Conflicts across endeavours escalate to a higher ordinal level (n+1).
* **Comprehensiveness** – More comprehensive endeavours override less comprehensive ones.
* **Assessment Endeavours** – Exogenous evaluators (law, morality, peer review) override their targets.

---

### Stoic Axioms

The system embeds Stoic principles as logical axioms:

1. **Encompassment** – Practical reasoning is the most comprehensive endeavour.
2. **Finality** – Nothing overrides all-things-considered practical reasoning.
3. **Moral Priority** – Moral norms are always superordinate to subscripted ones.
4. **Moral Rank** – For moral norms: **R > O > I**.
5. **Closure** – If no norm applies, default to *ought-not*.
6. **Futility** – Impossible norms yield prohibitions.

---

### Practical Effect

TallMountain’s calculus ensures that:

* Normative conflicts are preserved until explicitly resolved.
* The system can acknowledge genuine ethical dilemmas instead of erasing them.
* All reasoning eventually escalates to a **moral-level requirement/ought/indifference** reflecting Stoic “all-things-considered” judgment.

---

## Architecture

The system runs on a **cognitive pipeline** with three processing stages:

1. **Reactive** — immediate threat and risk scanning (e.g. prompt injection, unsafe content).
2. **Deliberative** — reasoning and planning across possible actions.
3. **Normative** — applying the Normative Calculus to ensure ethical compliance and resolve trade-offs.

### Core Components

* **Normative Agent**: loads and reasons over ethical propositions (virtue / norm / external), resolves conflicts.
* **Risk / Impact Analysis Engine**: evaluates potential harms, benefits, societal impact of requests.
* **LLM Interface**: connects to one or more LLMs (e.g. OpenAI, Mistral) for generating / interpreting text. Outputs are constrained via the ethical modules.
* **Interfaces**: REPL, REST API server, Web chat UI.
* **Configuration**: JSON and `.ini` files define normative propositions, thresholds, and ethical rules.

---

## Features

* Ethical risk assessment & conflict detection
* User intent analysis (detects risky or ambiguous requests)
* Multiple LLM support, structured responses (via Pydantic)
* Configurable safety / risk thresholds & rejection strategies
* REST, REPL, and Web Chat interfaces

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

Commands include:

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

* `POST /chat`  — send a message and receive ethically-filtered response

### Web Chat UI

```bash
python -m invoke chat-ui
```

Navigate to `http://localhost:5000` (or configured port) to use the browser-based chat interface.

---

## Configuration

* Config file at `src/config/app.ini` (or similar) for LLM settings, risk thresholds, etc.
* Normative frameworks loaded via JSON files: e.g. `src/config/system_endeavours.json`, `src/config/highest_endeavor.json`.
* Adjust rejection behavior, risk levels, etc., via configuration.

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

---

## References

[1]: https://link.springer.com/article/10.1023/A:1013805017161
[2]: https://www.jstor.org/stable/j.ctt1pd2k82
[3]: https://books.google.ie/books/about/The_Psychology_of_Narrative_Thought.html?id=4CdxQgAACAAJ

---

## License

MIT License

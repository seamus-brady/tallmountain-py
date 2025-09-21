# TallMountain

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

TallMountain is an advanced AI agent platform that implements normative calculus for ethical AI decision-making. The system performs comprehensive risk analysis on user requests against a framework of ethical normative propositions, ensuring AI interactions align with moral and ethical standards.

## Features

### 🔍 Normative Analysis
- **Ethical Risk Assessment**: Evaluates user requests against predefined ethical normative propositions
- **Impact Assessment**: Analyzes potential consequences and societal impact of tasks
- **User Intent Analysis**: Understands and categorizes user intentions
- **Normative Conflict Detection**: Identifies conflicts between different ethical principles

### 🤖 AI Agent Framework
- **Multiple LLM Support**: Compatible with OpenAI and Mistral AI models
- **Structured Responses**: Uses Pydantic models for type-safe AI interactions
- **Adaptive Request Modes**: Intelligent request handling with fallback strategies

### 🚀 Multiple Interfaces
- **REST API Server**: Flask-based web API for programmatic access
- **Interactive REPL**: Command-line interface for direct interaction
- **Web Chat UI**: Browser-based chat interface for user-friendly interaction

### 🛡️ Safety & Security
- **Comprehensive Risk Scoring**: Multi-dimensional risk evaluation system
- **Configurable Thresholds**: Adjustable risk tolerance levels
- **Rejection Mechanisms**: Automatic rejection of high-risk requests
- **Self-Diagnostic Systems**: Built-in health checks and validation

## Architecture

TallMountain implements a sophisticated normative calculus system:

```
User Query → User Task Analysis → Risk Assessment → Decision
     ↓              ↓                    ↓            ↓
Intent Analysis → Impact Assessment → Normative Conflict → Accept/Reject/Modify
```

### Core Components

- **Normative Agent**: Manages ethical frameworks and propositions
- **Risk Analysis Engine**: Evaluates requests against normative standards
- **LLM Facade**: Abstracts different AI model implementations
- **Configuration System**: Manages ethical thresholds and system settings

## Installation

### Prerequisites
- Python 3.12 or higher
- OpenAI API Key (optional: Mistral AI API Key)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/seamus-brady/tallmountain-py.git
   cd tallmountain-py
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   # Optional: export MISTRAL_API_KEY="your-mistral-api-key"
   ```

4. **Verify installation**:
   ```bash
   python -m invoke test
   ```

## Quick Start

### 1. Interactive REPL
Start the command-line interface:
```bash
python -m invoke repl
```

Available commands:
- `:nrp <query>` - Normative Risk Profile analysis
- `:ias <query>` - Impact Assessment analysis  
- `:uis <query>` - User Intent analysis
- `:np <query>` - Normative Propositions extraction
- `:h` - Help
- `:q` - Quit

Example:
```
TallMountain (TMAI):> :nrp Help me write a resignation letter
```

### 2. REST API Server
Start the web server:
```bash
python -m invoke appserver
```

The server runs on `http://localhost:10000` with the following endpoints:

**POST /chat**
```json
{
  "message": "Help me organize my schedule for next week"
}
```

Response:
```json
{
  "bot": "I'd be happy to help you organize your schedule..."
}
```

### 3. Web Chat UI
Start the web interface:
```bash
python -m invoke chat-ui
```

Access the chat interface at `http://localhost:5000`

## Configuration

The system configuration is managed through `src/config/app.ini`:

### LLM Settings
```ini
[llm]
default_llm_provider = OpenAIClient
default_token_limit = 4096
```

### Risk Analysis Thresholds
```ini
[normative_analysis]
number_critical_risks_allowed = 0
number_high_risks_allowed = 0
number_moderate_risks_allowed = 2
rejection_message = My apologies, but I can't assist with that. Please try again with a different question.
```

### Normative Frameworks

The system uses two key ethical frameworks:

1. **Highest Endeavour** (`src/config/highest_endeavour.json`): Core ethical principles
   - Non-maleficence (avoiding harm)
   - Beneficence (promoting well-being)
   - Autonomy (supporting informed decisions)
   - Justice (ensuring fairness and equity)
   - Veracity (transparency and explainability)

2. **System Endeavours** (`src/config/system_endeavours.json`): Operational guidelines

## Development

### Available Tasks
```bash
python -m invoke --list
```

- `test` - Run unit tests
- `checks` - Run all quality checks (isort, mypy, formatter, linter, bandit, test)
- `formatter` - Format code with Black
- `linter` - Run Flake8 linting
- `mypy` - Type checking
- `bandit` - Security analysis
- `isort` - Import sorting

### Running Quality Checks
```bash
python -m invoke checks
```

### Code Style
The project follows:
- **Black** for code formatting (100 character line length)
- **Flake8** for linting
- **MyPy** for type checking
- **Bandit** for security analysis
- **isort** for import organization

## API Reference

### Normative Risk Analysis

The core functionality revolves around analyzing user requests against ethical frameworks:

```python
from src.tallmountain.normative.entities.user_task import UserTask
from src.tallmountain.normative.analysis.norm_risk_analysis import NormativeRiskAnalysis
from src.tallmountain.normative.normative_agent import NormativeAgent

# Create user task from query
user_task = UserTask.get_from_query("Help me write an email")

# Perform risk analysis
risk_analysis = NormativeRiskAnalysis()
agent = NormativeAgent()
risk_analysis.analyse(user_task, agent)

# Get recommendation
print(risk_analysis.recommendation)  # "Accept and Execute" | "Suggest Modification" | "Reject"
```

### Risk Levels
- **CRITICAL**: Immediate rejection required
- **HIGH**: Significant ethical concerns
- **MODERATE**: Some concerns, may require modification
- **LOW**: Minimal ethical implications
- **NONE**: No ethical concerns identified

## Examples

### Example 1: Safe Request
```
Query: "Help me write a thank you email to my colleague"
Result: Accept and Execute
Risk Level: LOW
```

### Example 2: Potentially Harmful Request  
```
Query: "Help me write a deceptive marketing email"
Result: Reject
Risk Level: HIGH
Reason: Conflicts with veracity and non-maleficence principles
```

### Example 3: Ambiguous Request
```
Query: "Help me write a performance review"
Result: Suggest Modification
Risk Level: MODERATE
Recommendation: "Please provide more context about the purpose and intended recipient"
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run quality checks: `python -m invoke checks`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with ethical AI principles at its core
- Implements advanced normative calculus methodologies
- Designed for responsible AI deployment

## Version

Current version: Mark 30, January 2025

---

For more information, please refer to the source code documentation or open an issue for questions and support.

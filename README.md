# 🔍 Lightman AI
![Build Status](https://github.com/elementsinteractive/lightman-ai/actions/workflows/test.yml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/lightman-ai)](https://pypi.org/project/lightman-ai/)
[![Docker version](https://img.shields.io/docker/v/elementsinteractive/lightman-ai?label=DockerHub&logo=docker&logoColor=f5f5f5)](https://hub.docker.com/r/elementsinteractive/lightman-ai)
[![Python Version](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue?logo=python&logoColor=yellow)](https://pypi.org/project/lightman-ai/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/github/license/elementsinteractive/lightman-ai)](LICENSE)


> LLM-Powered Cybersecurity News Intelligence Platform

---

Lightman AI is an intelligent cybersecurity news aggregation and risk assessment platform that helps organizations stay ahead of potential security threats. By leveraging advanced AI agents, it automatically monitors cybersecurity news sources, analyzes content for relevance, and integrates with service desk systems for streamlined threat intelligence workflows.

## ✨ Key Features

- 🤖 **AI-Powered Classification**: Uses OpenAI GPT and Google Gemini models to intelligently classify cybersecurity news
- 📰 **Automated News Aggregation**: Monitors multiple cybersecurity news sources (TheHackerNews for now)
- 🎯 **Risk Scoring**: Configurable relevance scoring to filter noise and focus on critical threats
- 🔗 **Service Desk Integration**: Automatically creates tickets for identified security risks
- 📊 **Evaluation Framework**: Built-in tools to test and optimize AI agent performance
- ⚙️ **Flexible Configuration**: TOML-based configuration with multiple prompt templates
- 🚀 **CLI Interface**: Simple command-line interface for automation and scripting


## 📖 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [AI Agents & Models](#-ai-agents--models)
- [Evaluation & Testing](#-evaluation--testing)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#license)

## 🚀 Quick Start

### Installation

#### pip

1. **Install Lightman AI**:
   ```bash
   pip install lightman_ai
   ```

2. **Configure your AI agent** (OpenAI or Gemini):
   ```bash
   export OPENAI_API_KEY="your-api-key"
   # or
   export GOOGLE_API_KEY="your-api-key"
   ```

   or store you API KEYs in a .env file
   ```bash
   OPENAI_API_KEY="your-api-key"
   # or
   GOOGLE_API_KEY="your-api-key"
   ```

3. **Run the scanner**:
   ```bash
   lightman run --agent openai --score 7
   ```
   or let it pick up the default values from your `lightman.toml` file
   ```bash
   lightman run
   ```
#### Docker
1. **Pull the image**
   ```bash
   docker pull elementsinteractive/lightman-ai:latest
   ```

2. **Create configuration file**:
   ```bash
   echo '[default]
   agent = "openai"
   score_threshold = 8
   prompt = "development"
   
   [prompts]
   development = "Analyze cybersecurity news for relevance to our organization."' > lightman.toml
   ```

3. **Run with Docker**:

   ```bash
   docker run --rm \
     -v $(pwd)/lightman.toml:/app/lightman.toml \
     -e OPENAI_API_KEY="your-api-key" \
     elementsinteractive/lightman-ai:latest \
     run --config-file /app/lightman.toml --score 8 --agent openai
   ```
   
   You use a .env file instead of setting the environment variables through the cli
   
   ```bash
      cp .env.example .env
   ```
   
   Fill it with your values and run:
   
   ```bash
   docker run --rm \
     -v $(pwd)/lightman.toml:/app/lightman.toml \
     --env-file .env \
     elementsinteractive/lightman-ai:latest \
     run --config-file /app/lightman.toml --score 8 --agent openai
   ``` 

## 🔧 Usage

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--agent` | AI agent to use (`openai`, `gemini`) | From config file |
| `--score` | Minimum relevance score (1-10) | From config file |
| `--prompt` | Prompt template name | From config file |
| `--config-file` | Path to configuration file | `lightman.toml` |
| `--config` | Configuration section to use | `default` |
| `--env-file` | Path to environment variables file | `.env` |
| `--dry-run` | Preview results without taking action | `false` |
| `--prompt-file` | File containing prompt templates | `lightman.toml` |
| `--start-date` | Start date to retrieve articles | False |
| `--today` | Retrieve articles from today | False |
| `--yesterday` | Retrieve articles from yesterday | False |
| `-v` | Be more verbose on output | False |


### Environment Variables:
lightman-ai uses the following environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key
- `GOOGLE_API_KEY` - Your Google Gemini API key
- `SERVICE_DESK_URL` - Service desk instance URL (optional)
- `SERVICE_DESK_USER` - Service desk username (optional)
- `SERVICE_DESK_TOKEN` - Service desk API token (optional)
- `TIME_ZONE` - Your time zone (optional, defaults to UTC. i.e. "Europe/Amsterdam".)

By default, it will try to load a `.env` file. You can also specify a different path with the `--env-file` option.


## ⚙️ Configuration

Lightman AI uses TOML configuration files for flexible setup. Create a `lightman.toml` file:

```toml
[default]
agent = 'openai'              # AI agent to use (openai, gemini)
score_threshold = 8           # Minimum relevance score (1-10)
prompt = 'development'        # Prompt template to use

# Optional: Service desk integration
service_desk_project_key = "SEC"
service_desk_request_id_type = "incident"

# alternative configuration
[malware]
agent = 'openai'              # AI agent to use (openai, gemini)
score_threshold = 8           # Minimum relevance score (1-10)
prompt = 'malware'            # Prompt template to use

# Optional: Service desk integration
service_desk_project_key = "SEC"
service_desk_request_id_type = "incident"

[prompts]
development = """
Analyze the following cybersecurity news articles and determine their relevance to our organization.
Rate each article from 1-10 based on potential impact and urgency.
Focus on vulnerabilities."""

malware = """
Analyze the following cybersecurity news articles and determine their relevance to our organization.
Rate each article from 1-10 based on potential impact and urgency.
Focus on malware."""

custom_prompt = """
Your custom analysis prompt here...
"""
```
Note how it supports different configurations and prompts.


It also supports having separate files for your prompts and your configuration settings. Specify the path with `--prompt`.

`lightman.toml`
```toml
[default]
agent = 'openai'              # AI agent to use (openai, gemini)
score_threshold = 8           # Minimum relevance score (1-10)
prompt = 'development'        # Prompt template to use

# Optional: Service desk integration
service_desk_project_key = "SEC"
service_desk_request_id_type = "incident"
```

`prompts.toml`
```toml
[prompts]
development = """
Analyze the following cybersecurity news articles and determine their relevance to our organization.
Rate each article from 1-10 based on potential impact and urgency.
Focus on: data breaches, malware, vulnerabilities, and threat intelligence.
"""

custom_prompt = """
Your custom analysis prompt here...
"""
```

### Examples
```bash
# Run with default settings
lightman run

# Use specific AI agent and score threshold
lightman run --agent gemini --score 7

# Use custom prompt template
lightman run --prompt custom_prompt --config-file ./my-config.toml

# Use custom environment file
lightman run --env-file production.env --agent openai --score 8

# Dry run (preview results without creating service desk tickets)
lightman run --dry-run --agent openai --score 9

# Retrieve all the news from today
lightman run --agent openai --score 8 --prompt security_critical --today

# Retrieve all the news from yesterday
lightman run --agent openai --score 8 --prompt security_critical --yesterday
```


### Development Installation
In order to fully use the provided setup for local development and testing, this project requires the following dependencies:
- [Python 3.13](https://www.python.org/downloads/release/python-3130/)
- [just](https://github.com/casey/just)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

Then simply:
```bash
git clone git@github.com:elementsinteractive/lightman-ai.git
cd lightman_ai
just venv  # Creates virtual environment and installs dependencies
just test  # Runs the tests
just eval  # Runs the evaluation framework
```

## 📊 Evaluation & Testing

Lightman AI includes a comprehensive evaluation framework to test and optimize AI agent performance:

### Running Evaluations

```bash
# Evaluate agent performance
just eval --agent openai --samples 3 --score 7

# Compare different agents
just eval --agent gemini --samples 5 

# Add tags to differentiate runs from one another
just eval --agent gemini --samples 5 --tag "first-run"
just eval --agent gemini --samples 5 --tag "second-run"

# Test custom prompts
just eval --prompt custom_security --samples 10

# Use custom environment file for evaluation
python -m eval.cli --env-file production.env --agent openai --samples 3
```

You can also provide defaults in a `toml` file for `eval`.

```toml
[eval]
agent = 'openai'
score_threshold = 8
prompt = 'classify'
samples = 3
```

### Evaluation Metrics

The evaluation system measures:
- **Precision**: Accuracy of threat identification
- **Recall**: Coverage of actual security threats
- **F1 Score**: Balanced performance metric
- **Score Distribution**: Analysis of relevance scoring patterns

### Evaluation Dataset

For precision evaluation, Lightman AI uses a curated set of **unclassified cybersecurity articles** that serve as ground truth data. These articles include:

- **Real-world news articles** from various cybersecurity sources
- **Mixed relevance levels** - both highly relevant and irrelevant security news
- **Diverse threat categories** - malware, data breaches, vulnerabilities, policy changes
- **Pre-validated classifications** by security experts for accuracy benchmarking

The evaluation framework compares the AI agent's classifications against these known classifications to measure:
- How accurately the agent identifies truly relevant threats (precision)
- How well it avoids false positives from irrelevant news
- Consistency across different types of security content

This approach ensures that performance metrics reflect real-world usage scenarios where the AI must distinguish between various types of cybersecurity news content.

**Make sure to fill in the `RELEVANT_ARTICLES` with the ones you classify as relevant, so that you can compare the accuracy after running the `eval` script.*** 

## Sentry 
Sentry is **optional**: the application does not require it to function, and all features will work even if Sentry is not configured or fails to start.
If you install the project via pip and want Sentry installed, run:

```bash
   pip install lightman-ai[sentry]
```
Sentry comes by default with the Docker image. If you don't want to use it, simply do not set `SENTRY_DSN` env variable.

The application will automatically pick up and use environment variables if they are present in your environment or `.env` file.
To enable Sentry, set the `SENTRY_DSN` environment variable. This is **mandatory** for Sentry to be enabled. If `SENTRY_DSN` is not set, Sentry will be skipped and the application will run normally.
If Sentry fails to initialize for any reason (e.g., network issues, invalid DSN), the application will log a warning and continue execution without error monitoring, and logging to stdout.

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TheHackerNews** for providing cybersecurity news data


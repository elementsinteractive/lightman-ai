# 🔍 Lightman AI

> **AI-Powered Cybersecurity News Intelligence Platform*

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

### pip

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

### Docker

1. **Create configuration file**:
   ```bash
   echo '[default]
   agent = "openai"
   score_threshold = 8
   prompt = "development"
   
   [prompts]
   development = "Analyze cybersecurity news for relevance to our organization."' > lightman.toml
   ```

2. **Run with Docker**:
   ```bash
   docker run --rm \
     -v $(pwd)/lightman.toml:/app/lightman.toml \
     -e OPENAI_API_KEY="your-api-key" \
     elementsinteractive/lightman-ai:latest \
     lightman run --config-file /app/lightman.toml --score 7
   ```

4. **View results**: Lightman will analyze cybersecurity news and output relevant articles that meet your score threshold.

## 📥 Installation

### Docker
Lightman AI has an available Docker image on Docker Hub:

```bash
# Pull the latest image
docker pull elementsinteractive/lightman-ai:latest

# Create your configuration file

   echo '[default]
   agent = "openai"
   score_threshold = 8
   prompt = "development"
   
   [prompts]
   development = "Analyze cybersecurity news for relevance to our organization."' > lightman.toml
   ```


# Run with mounted configuration
```bash
docker run -d \
  --name lightman-ai \
  -v $(pwd)/lightman.toml:/app/lightman.toml \
  -e OPENAI_API_KEY="your-api-key" \
  elementsinteractive/lightman-ai:latest \
  lightman run --config-file /app/lightman.toml
```

**Docker Environment Variables:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `GOOGLE_API_KEY` - Your Google Gemini API key
- `SERVICE_DESK_URL` - Service desk instance URL (optional)
- `SERVICE_DESK_USER` - Service desk username (optional)
- `SERVICE_DESK_TOKEN` - Service desk API token (optional)



### Development Installation
```bash
git clone git@github.com:elementsinteractive/lightman-ai.git
cd lightman_ai
just venv  # Creates virtual environment and installs dependencies
```

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
### Environment Variables

Set up your AI provider credentials:

```bash
# For OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# For Google Gemini
export GOOGLE_API_KEY="your-google-api-key"

# Optional: Service desk integration
export SERVICE_DESK_URL="https://your-company.atlassian.net"
export SERVICE_DESK_USER="your-username"
export SERVICE_DESK_TOKEN="your-api-token"

```
You can also specify a different path for your .env file with the `--env-file` option


## 🔧 Usage

### Basic Usage

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
```

### Command Line Options

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

### Example Workflows

**Daily Security Monitoring**:
```bash
# Local installation
lightman run --agent openai --score 8 --prompt security_critical

# With custom environment file
lightman run --env-file production.env --agent openai --score 8

# Docker 
docker run --rm \
  -v $(pwd)/lightman.toml:/app/lightman.toml \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  elementsinteractive/lightman-ai:latest \
  lightman run --config-file /app/lightman.toml --score 8
```


**Weekly Risk Assessment**:
```bash
# Local installation
lightman run --agent gemini --score 6 --prompt weekly_assessment

# With environment-specific settings
lightman run --env-file weekly.env --agent gemini --score 6

# Docker 
docker run --rm \
  -v $(pwd)/lightman.toml:/app/lightman.toml \
  -e GOOGLE_API_KEY="$GOOGLE_API_KEY" \
  elementsinteractive/lightman-ai:latest \
  lightman run --config-file /app/lightman.toml --agent gemini --score 6
```

**Integration Testing**:
```bash
# Test configuration without creating tickets
lightman run --dry-run --config testing

# Test with staging environment
lightman run --env-file staging.env --dry-run --config testing
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

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TheHackerNews** for providing cybersecurity news data


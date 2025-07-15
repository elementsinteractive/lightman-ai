# 🤝 Contributing to Lightman AI

Thank you for your interest in contributing to Lightman AI! We welcome contributions from the community and are grateful for any help you can provide.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Contributions](#making-contributions)
- [Contribution Types](#contribution-types)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and inclusive in all interactions.

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- [Poetry](https://python-poetry.org/) for dependency management
- [Just](https://github.com/casey/just) for task automation
- Git for version control

### Development Setup

1. **Fork the repository** on GitLab
2. **Clone your fork**:
   ```bash
   git clone https://gitlab.com/your-username/lightman_ai.git
   cd lightman_ai
   ```

3. **Set up the development environment**:
   ```bash
   # Install just (macOS)
   brew install just
   
   # Install just (Ubuntu/Debian)
   snap install --edge --classic just
   
   # Create virtual environment and install dependencies
   just venv
   ```

4. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On Linux/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

5. **Verify installation**:
   ```bash
   just test
   ```

## 🛠️ Making Contributions

### Before You Start

1. **Check existing issues** to see if your idea is already being discussed
2. **Create an issue** for new features or bug reports
3. **Discuss your approach** before making significant changes

### Branch Naming Convention

Use descriptive branch names that follow this pattern:
- `feature/description-of-feature`
- `fix/description-of-fix`
- `docs/description-of-docs-change`
- `refactor/description-of-refactor`

Examples:
```bash
git checkout -b feature/add-claude-ai-support
git checkout -b fix/evaluation-memory-leak
git checkout -b docs/improve-docker-setup
```

## 🎯 Contribution Types

### 🐛 Bug Fixes
- Fix existing functionality that isn't working as expected
- Include test cases that reproduce the bug
- Update documentation if necessary

### ✨ New Features
- Add new AI agent integrations
- Implement new news sources
- Add evaluation metrics
- Enhance CLI functionality

### 📚 Documentation
- Improve README, API docs, or inline comments
- Add examples and tutorials
- Fix typos and clarify instructions

### 🧪 Tests
- Add missing test coverage
- Improve existing tests
- Add integration tests

### 🏗️ Infrastructure
- CI/CD improvements
- Docker enhancements
- Build process optimizations

## 📝 Pull Request Process

### 1. Prepare Your Changes

```bash
# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Format code
just format

# Run linting
just lint

# Run tests
just test-all

# Commit your changes
git add .
git commit -m "feat: add support for Claude AI models"
```

### 2. Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(agent): add Claude AI integration
fix(cli): resolve config file parsing issue
docs(readme): update installation instructions
test(eval): add integration tests for gemini agent
```

### 3. Submit Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a merge request** on GitLab with:
   - Clear title and description
   - Reference to related issues
   - Screenshots (if applicable)
   - Testing instructions

3. **Request review** from maintainers

### 4. Address Feedback

- Respond to review comments promptly
- Make requested changes
- Update tests and documentation as needed
- Push updates to the same branch

## 🔧 Code Standards

### Python Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **Ruff** for linting
- **mypy** for type checking

Run all checks:
```bash
just format  # Format code with black and isort
just lint    # Run ruff and mypy
```

### Code Structure

```python
# Type hints are required for all public functions
def process_articles(articles: ArticlesList, agent: BaseAgent) -> SelectedArticlesList:
    """Process articles using the specified AI agent.
    
    Args:
        articles: List of articles to process
        agent: AI agent to use for classification
        
    Returns:
        List of selected articles with relevance scores
        
    Raises:
        AgentError: If the agent fails to process articles
    """
    # Implementation here
```

### Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately

```python
from lightman_ai.core.exceptions import ConfigNotFoundError

try:
    config = load_config(path)
except FileNotFoundError as e:
    raise ConfigNotFoundError(f"Config file not found: {path}") from e
```

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies

```python
def test_openai_agent_classifies_articles_correctly():
    """Test that OpenAI agent correctly classifies relevant articles."""
    # Arrange
    agent = OpenAIAgent(system_prompt="Test prompt")
    articles = create_test_articles()
    
    # Act
    result = agent.get_prompt_result(str(articles))
    
    # Assert
    assert len(result.selected_articles) > 0
    assert all(article.score >= 7 for article in result.selected_articles)
```

### Running Tests

```bash
# Run all tests
just test

# Run specific test file
just test tests/ai/test_openai_agent.py

# Run with coverage
just test-all

# Run evaluation tests
just eval --samples 1 --agent openai
```

### Test Coverage

- Maintain >90% test coverage
- Focus on critical paths and edge cases
- Include integration tests for major features

## 📖 Documentation

### Code Documentation

- Use clear, descriptive docstrings
- Document all public APIs
- Include examples where helpful

### README Updates

- Update README for new features
- Add configuration examples
- Update CLI documentation

### API Documentation

- Update API docs for new endpoints
- Include request/response examples
- Document error responses

## 🏗️ Development Workflow

### Daily Development

```bash
# Start working
git checkout main
git pull origin main
git checkout -b feature/my-feature

# Make changes
# ... edit code ...

# Test changes
just test-all
just format
just lint

# Commit and push
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature
```

### Working with AI Agents

When adding new AI agent support:

1. **Create agent class** in `src/lightman_ai/ai/provider/`
2. **Inherit from BaseAgent** and implement required methods
3. **Add to agent utils** in `src/lightman_ai/ai/utils.py`
4. **Write comprehensive tests** in `tests/ai/provider/`
5. **Update documentation** with usage examples

### Adding News Sources

When adding new news sources:

1. **Create source class** in `src/lightman_ai/sources/`
2. **Implement required interface** methods
3. **Add configuration options** if needed
4. **Write tests** with mocked responses
5. **Update documentation** and examples

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in pyproject.toml
- [ ] Git tag created
- [ ] Docker image updated

## 📞 Getting Help

### Communication Channels

- **Issues**: For bug reports and feature requests
- **Merge Requests**: For code contributions
- **Email**: For security issues or private matters

### Questions?

- Check existing [issues](https://gitlab.com/makerstreet-development/elements/backend/lightman_ai/-/issues)
- Create a new issue with the "question" label
- Review the [documentation](https://makerstreet-development.gitlab.io/elements/backend/lightman_ai)

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project acknowledgments

Thank you for contributing to Lightman AI! 🎉

---

**Happy coding!** 🚀

# Contributing to Photo Organizer

Thank you for your interest in contributing to Photo Organizer! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/photo-organizer.git
   cd photo-organizer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install in development mode**
   ```bash
   pip install -e .
   ```

## Code Style

- Use Python 3.7+ features
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

## Testing

Before submitting a pull request, please ensure:

1. Your code works with different image formats
2. Error handling is proper
3. Documentation is updated
4. Code follows the existing style

## Areas for Contribution

We'd love help with:

- **Improving classification accuracy**
- **Adding new image categories**
- **Performance optimizations**
- **Better error handling**
- **Documentation improvements**
- **Adding tests**
- **UI/Web interface**
- **Mobile app version**

## Questions?

Don't hesitate to ask questions by creating an issue with the "question" label.

## Code of Conduct

Please be respectful and constructive in all interactions. We want to maintain a welcoming environment for all contributors.

Thank you for contributing! 🎉

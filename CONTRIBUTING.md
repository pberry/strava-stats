# Contributing to Strava Stats

Thank you for your interest in contributing to Strava Stats! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open a GitHub issue with:

- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant error messages or logs

### Suggesting Enhancements

Have an idea for a new feature or improvement? Open a GitHub issue with:

- A clear description of the proposed feature
- Why this feature would be useful
- Any examples or mockups if applicable

### Pull Requests

We welcome pull requests! Here's the process:

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**:
   - Write clear, concise commit messages
   - Add tests for new functionality
   - Ensure all tests pass: `pytest`

3. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```

4. **Open a Pull Request**:
   - Provide a clear description of the changes
   - Reference any related issues
   - Explain the motivation behind the changes

### Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/strava-stats.git
   cd strava-stats
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests to ensure everything works:
   ```bash
   pytest
   ```

### Testing

- All new features should include tests
- Run the test suite before submitting a PR: `pytest`
- Ensure tests pass and there are no regressions

### Commit Messages

Write clear, descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep the first line under 72 characters
- Reference issues and pull requests when relevant

Example:
```
Add support for cycling activity reports

- Add cycling to activity types in combined_report.py
- Update tests to include cycling scenarios
- Update documentation

Fixes #123
```

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

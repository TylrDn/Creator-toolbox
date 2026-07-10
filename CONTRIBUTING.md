# Contributing to Creator Toolbox

## Overview

Creator Toolbox is a coordinated system for creator-economy launch orchestration.
Contributions should enhance the architecture, documentation, product modules, or
test coverage.

## Branch Workflow

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make coherent, atomic commits
3. Push to your fork
4. Open a pull request against `main`
5. Address review feedback
6. Merge via squash or rebase to keep history clean

## Local Setup

```bash
# Clone the repository
git clone https://github.com/TylrDn/Creator-toolbox.git
cd Creator-toolbox

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_router.py -v

# Run tests with coverage
pytest tests/ --cov=orchestrator
```

## Code Style

- Use Python 3.11+ syntax
- Follow PEP 8 conventions
- Type hints are encouraged but not required
- Keep comments sparse and useful
- Variable names should be explicit

## Commit Guidance

1. Write clear, imperative commit messages
2. Reference related issues: `Fixes #123`
3. Keep commits focused on one logical change
4. Example: `feat: add critic agent IP-safety blocking`

## Documentation

- Update README if structure changes
- Add docstrings to new functions
- Update relevant docs/ files for architectural changes
- Use plain English in all documentation

## Submitting a Pull Request

1. Fill out the PR template completely
2. Link related issues
3. Describe what changed and why
4. Include any breaking changes
5. Request reviewers

## Architecture Principles

When contributing, keep these principles in mind:

- **Clarity over cleverness**: code should be easy to understand
- **Game-agnostic by design**: use config to parameterize game-specific behavior
- **IP-safe by default**: enforce safety rules in the orchestrator
- **Local-first and testable**: prefer offline, testable work
- **Structured over magical**: explicit is better than implicit

## Questions?

Open an issue for questions or design discussions before starting major work.

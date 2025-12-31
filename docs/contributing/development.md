# Development Setup

Guide for contributors and developers.

## Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/EsOsO/ShiroInk.git
cd ShiroInk

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-docs.txt  # For documentation

# Run tests
python -m unittest discover -s . -p 'test_*.py' -v
```

## Running Locally

```bash
export PYTHONPATH=src
python src/main.py input/ output/ --pipeline kindle --dry-run
```

## Contributing

Please follow [Conventional Commits](conventional-commits.md) for commit messages.

## Testing

```bash
# Unit tests
PYTHONPATH=src python -m unittest discover -s . -p 'test_*.py'

# Build Docker image
docker build -t shiroink:dev .

# Test Docker image
docker run --rm shiroink:dev --version
```

## Documentation

```bash
# Install docs dependencies
pip install -r requirements-docs.txt

# Serve docs locally
mkdocs serve

# Build docs
mkdocs build
```

Visit http://127.0.0.1:8000 to view documentation.

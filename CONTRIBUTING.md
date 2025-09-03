# Contributing

Thanks for helping improve **borica-qes**!

We welcome bug reports, feature requests, and pull requests. To make the process smooth, please follow these guidelines.

## Getting Started

1. Fork the repository and clone your fork locally.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   pre-commit install
   ```
3. Run the test suite to ensure your environment is set up correctly:
   ```bash
   pytest
   ```

## Pull Requests

- **Small, focused changes**: Keep pull requests small and targeted to a single issue or feature.
- **Tests**: Add tests to cover your changes. We use `pytest` with `httpx.MockTransport`.
- **Type and lint**: Ensure `ruff`, `black`, and `pyright` are happy by running:
  ```bash
  ruff check .
  black --check .
  pyright
  ```
- **Docs**: For user‑facing changes, update the README or docs under `docs/`.
- **Changelog**: Add an entry in `CHANGELOG.md` under the `Unreleased` section.

## Issues

When filing an issue, please include:

- A clear description of the problem or request.
- Steps to reproduce (for bugs) including versions used.
- Any relevant error messages or stack traces.

Thank you for your contributions and for making this project better!
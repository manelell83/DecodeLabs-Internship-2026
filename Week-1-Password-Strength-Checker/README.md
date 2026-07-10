# Password Strength Analyzer

A professional desktop application for analyzing password strength with entropy estimation, threat modeling, and modern UI design.

## Overview

This project demonstrates a portfolio-quality cybersecurity utility built in Python. It provides a polished interface for evaluating password robustness in real time and offers actionable recommendations for improvement.

## Features

- Real-time password evaluation while typing
- Modern dark-themed desktop interface
- Strength score from 0 to 100
- Entropy estimation in bits
- Detailed checklist for common password requirements
- Detection of repeated patterns, keyboard walks, years, and name-like terms
- Suggested improvements for stronger credentials
- Secure password generation
- JSON export of analysis results

## Architecture

- app.py: application entry point
- core/password_analyzer.py: scoring, entropy, heuristics, and password generation
- gui/main_window.py: desktop interface and event handling
- data/common_passwords.txt: known weak password corpus
- tests/test_passwords.py: unit tests for analyzer behavior

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

## Usage

- Type a password into the input field.
- Review the score, entropy, checklist, and improvement suggestions.
- Use the secure password generator or export the analysis to JSON.

## Future Improvements

- Add password breach lookup integration
- Support password history and reuse checks
- Introduce localization and theme switching
- Package the app into a native desktop installer

## Screenshots

Placeholder for screenshots to be added in future iterations.

## License

This project is licensed under the MIT License.
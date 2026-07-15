# CipherLab

CipherLab is a modern desktop application for learning and experimenting with classical ciphers such as Caesar and Vigenère. It is designed as a polished cybersecurity portfolio project while staying aligned with the internship requirement for basic encryption and decryption.

## Features

- Encrypt and decrypt text with Caesar cipher
- Encrypt and decrypt text with Vigenère cipher
- User-defined shift and keyword input
- Import and export text files
- Copy output to clipboard
- History tracking for all operations
- Dark mode and modern desktop UI
- Status bar and keyboard shortcuts

## Project Structure

```text
Project-02-Basic-Encryption-Decryption/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── assets/
├── core/
├── gui/
├── utils/
├── data/
└── tests/
```

## Installation

1. Create a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```

## Usage

- Choose the cipher mode from the sidebar
- Enter text and key information
- Click Encrypt or Decrypt
- Use file import/export actions when needed

## Future Improvements

- Add affine and XOR ciphers
- Add visual history charts
- Add stronger validation and logging

## License

MIT License

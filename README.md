# Cipher Web Application - Complete Standalone Version

A Flask-based web application for encryption and decryption using three classical cipher algorithms:
- **Vigenère Cipher**: Polyalphabetic substitution cipher using a keyword
- **Affine Cipher**: Monoalphabetic substitution cipher using mathematical functions
- **Playfair Cipher**: Digraph substitution cipher using a 5×5 matrix

## ✨ Features

- **Standalone Application**: No templates folder required - HTML is embedded in the Python file
- Clean, responsive web interface
- Real-time encryption and decryption
- Visual matrix display for Playfair cipher
- Error handling and validation
- Support for all three cipher types

## 📋 Requirements

- Python 3.7 or higher
- Flask (will be installed from requirements.txt)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install flask
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

Simply run the Python file:

```bash
python app.py
```

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

That's it! No templates folder, no static files - everything is in one file.

## 📖 Usage Guide

### Vigenère Cipher
- Enter your message in the text area
- Provide a keyword (e.g., "LEMON")
- Click "Encrypt" or "Decrypt"
- The cipher repeats the key to match the message length

**Example:**
- Plaintext: "HELLO"
- Key: "KEY"
- Ciphertext: "RIJVS"

### Affine Cipher
- Enter your message in the text area
- Provide two keys:
  - **Key a**: Must be coprime with 26 (e.g., 5, 7, 9, 11, etc.)
  - **Key b**: Any integer from 0-25 (e.g., 8)
- Click "Encrypt" or "Decrypt"

**Valid values for Key a:** 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25

**Example:**
- Plaintext: "HELLO"
- Keys: a=5, b=8
- Ciphertext: "RCLLA"

### Playfair Cipher
- Enter your message in the text area
- Provide a keyword (e.g., "MONARCHY")
- Click "Encrypt" or "Decrypt"
- The 5×5 matrix will be displayed
- Note: Letters I and J are treated as the same letter

**Example:**
- Plaintext: "HELLO"
- Key: "MONARCHY"
- Matrix will be shown
- Ciphertext: "GATLMQ"

## 🔧 API Endpoints

The application provides RESTful API endpoints that you can test with tools like Postman or curl:

### POST /api/vigenere
```json
{
  "message": "HELLO",
  "key": "KEY",
  "operation": "encrypt"
}
```

### POST /api/affine
```json
{
  "message": "HELLO",
  "a": 5,
  "b": 8,
  "operation": "encrypt"
}
```

### POST /api/playfair
```json
{
  "message": "HELLO",
  "key": "MONARCHY",
  "operation": "encrypt"
}
```

## 📁 Project Structure

```
cipher-web-app/
│
├── app.py                 # Complete standalone application (HTML + Python)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔐 How the Ciphers Work

### Vigenère Cipher
Uses a keyword to shift each letter of the plaintext. Each letter in the key determines the shift amount for the corresponding letter in the plaintext.

**Encryption:** C = (P + K) mod 26  
**Decryption:** P = (C - K) mod 26

### Affine Cipher
Uses two keys (a and b) in a mathematical formula. Key 'a' must be coprime with 26.

**Encryption:** E(x) = (ax + b) mod 26  
**Decryption:** D(y) = a⁻¹(y - b) mod 26

Where a⁻¹ is the modular multiplicative inverse of a.

### Playfair Cipher
Uses a 5×5 matrix generated from a keyword. Encrypts pairs of letters using position rules.

**Rules:**
1. Same row: Take letters to the right (wrap around)
2. Same column: Take letters below (wrap around)
3. Rectangle: Take letters on opposite corners

## ⚠️ Important Notes

- All ciphers work with alphabetic characters only
- Spaces and special characters are removed
- Output is in uppercase
- For educational purposes only - these are historical ciphers and not secure for modern use

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
Install Flask using: `pip install flask`

### "Python was not found..."
This is a Windows-specific error.
1. Try using `py app.py` instead of `python app.py`.
2. If that fails, install Python from python.org. **Important:** Check "Add Python to PATH" during installation.
3. Go to **Settings > Apps > Advanced app settings > App execution aliases** and turn **OFF** the toggles for `python.exe` and `python3.exe`.

### "Address already in use"
Another application is using port 5000. Either:
- Stop the other application
- Change the port in app.py: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Browser shows "Cannot connect"
Make sure:
1. The Flask server is running (you should see output in the terminal)
2. You're accessing the correct URL: http://localhost:5000
3. Your firewall isn't blocking the connection

## 💡 Tips

- Use the browser's developer console (F12) to debug any JavaScript errors
- Check the Flask console output for server-side errors
- Valid Affine cipher 'a' keys are: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
- For Playfair, remember that I and J are treated as the same letter

## 📝 License

This project is for educational purposes only.

---

**Enjoy encrypting! 🔐**

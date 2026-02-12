# Setup Instructions

## Project Structure

Your cipher web application should have this folder structure:

```
cipher-web-app/
│
├── app.py                    # Flask application (main file)
├── requirements.txt          # Python dependencies
├── README.md                # Documentation
│
└── templates/               # HTML templates folder
    └── index.html          # Main webpage
```

## Installation Steps

### Step 1: Create Project Folder

Create a folder for your project and place all the files in it:

```bash
mkdir cipher-web-app
cd cipher-web-app
```

### Step 2: Copy Files

Make sure you have these files in your project folder:
- `app.py` (the Flask backend)
- `requirements.txt` (dependencies)
- Create a folder named `templates`
- Put `index.html` inside the `templates` folder

**Important:** The `templates` folder MUST be in the same directory as `app.py`

### Step 3: Install Flask

Open terminal/command prompt in your project folder and run:

```bash
pip install flask
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 5: Open in Browser

Go to: **http://localhost:5000**

## File Locations (CRITICAL)

```
Your working directory/
│
├── app.py              ← Run this file
│
└── templates/          ← Must be named "templates"
    └── index.html      ← Your HTML file goes here
```

**Common Error:** If you see "TemplateNotFound", it means:
- The `templates` folder is missing
- The `templates` folder is in the wrong location
- The HTML file is not named `index.html`

## Testing the Application

### Test Vigenère Cipher
1. Click on "Vigenère Cipher" in the sidebar
2. Message: `HELLO WORLD`
3. Key: `KEY`
4. Click "Encrypt"
5. Result: `RIJVSUYVJN`

### Test Affine Cipher
1. Click on "Affine Cipher"
2. Message: `HELLO WORLD`
3. Key a: `5` (must be coprime with 26)
4. Key b: `8`
5. Click "Encrypt"
6. Result: `RCLLAOAPLX`

### Test Playfair Cipher
1. Click on "Playfair Cipher"
2. Message: `HELLO WORLD`
3. Key: `MONARCHY`
4. Click "Encrypt"
5. You'll see a 5×5 matrix and the encrypted result

## Troubleshooting

### Error: "TemplateNotFound: index.html"

**Solution:**
1. Create a folder named `templates` (lowercase, plural)
2. Put `index.html` inside the `templates` folder
3. Make sure `templates` is in the same directory as `app.py`

### Error: "Module not found: flask"

**Solution:**
```bash
pip install flask
```

### Error: "Address already in use"

**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access: http://localhost:5001

### Windows Users

If `pip` doesn't work:
```bash
py -m pip install flask
python app.py
```

### Mac/Linux Users

If you have permission issues:
```bash
pip3 install flask
python3 app.py
```

## Valid Affine Cipher Keys

Key 'a' must be coprime with 26. Valid values are:
**1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25**

Key 'b' can be any integer from 0-25.

## Features

✅ Three cipher algorithms (Vigenère, Affine, Playfair)  
✅ Clean responsive interface  
✅ Real-time encryption/decryption  
✅ Matrix visualization for Playfair  
✅ Input validation and error handling  
✅ RESTful API endpoints  

Enjoy! 🔐

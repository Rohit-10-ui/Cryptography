"""
Main Flask Application
Cipher Encryption/Decryption Service
"""

from flask import Flask, render_template, request, jsonify
from ciphers import vigenere, affine, playfair

app = Flask(__name__)

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

# ==================== VIGENERE CIPHER API ====================

@app.route('/api/vigenere', methods=['POST'])
def api_vigenere():
    """Handle Vigenere cipher encryption/decryption"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', '')
        
        if not message or not key:
            return jsonify({'error': 'Message and key are required'}), 400
        
        if operation == 'encrypt':
            result = vigenere.encrypt(message, key)
            return jsonify({'success': True, 'result': result, 'operation': 'Encrypted'})
        elif operation == 'decrypt':
            result = vigenere.decrypt(message, key)
            return jsonify({'success': True, 'result': result, 'operation': 'Decrypted'})
        else:
            return jsonify({'error': 'Invalid operation'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== AFFINE CIPHER API ====================

@app.route('/api/affine', methods=['POST'])
def api_affine():
    """Handle Affine cipher encryption/decryption"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        a = data.get('a')
        b = data.get('b')
        operation = data.get('operation', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        try:
            a = int(a)
            b = int(b)
        except (ValueError, TypeError):
            return jsonify({'error': 'Keys a and b must be integers'}), 400
        
        if not affine.validate_key_a(a):
            return jsonify({'error': 'Key a must be coprime with 26 (valid: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)'}), 400
        
        if operation == 'encrypt':
            result = affine.encrypt(message, a, b)
            return jsonify({'success': True, 'result': result, 'operation': 'Encrypted'})
        elif operation == 'decrypt':
            result = affine.decrypt(message, a, b)
            if result == "Invalid value of 'a'":
                return jsonify({'error': result}), 400
            return jsonify({'success': True, 'result': result, 'operation': 'Decrypted'})
        else:
            return jsonify({'error': 'Invalid operation'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PLAYFAIR CIPHER API ====================

@app.route('/api/playfair', methods=['POST'])
def api_playfair():
    """Handle Playfair cipher encryption/decryption"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', '')
        
        if not message or not key:
            return jsonify({'error': 'Message and key are required'}), 400
        
        if operation == 'encrypt':
            result, matrix = playfair.encrypt(message, key)
            matrix_str = playfair.format_matrix(matrix)
            return jsonify({
                'success': True,
                'result': result, 
                'operation': 'Encrypted',
                'matrix': matrix_str
            })
        elif operation == 'decrypt':
            result, matrix = playfair.decrypt(message, key)
            matrix_str = playfair.format_matrix(matrix)
            return jsonify({
                'success': True,
                'result': result, 
                'operation': 'Decrypted',
                'matrix': matrix_str
            })
        else:
            return jsonify({'error': 'Invalid operation'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SERVER ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
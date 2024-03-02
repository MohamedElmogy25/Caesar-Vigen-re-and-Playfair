from flask import Flask, render_template, request

app = Flask(__name__)

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def vigenere_cipher(text, key):
    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - offset + ord(key[key_index]) - ord('A')) % 26 + offset)
            key_index = (key_index + 1) % len(key)
        else:
            result += char

    return result

def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key += alphabet

    matrix = [key[i:i+5] for i in range(0, 25, 5)]
    return matrix

def playfair_cipher(text, key):
    def find_position(matrix, char):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j

    def same_row(i1, i2):
        return i1 == i2

    def same_column(j1, j2):
        return j1 == j2

    result = ""
    matrix = generate_playfair_matrix(key)

    text = text.upper().replace("J", "I")
    text = "".join([char if char.isalpha() else 'X' for char in text])

    for i in range(0, len(text), 2):
        char1 = text[i]
        char2 = text[i+1] if i+1 < len(text) else 'X'

        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)

        if same_row(row1, row2):
            result += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif same_column(col1, col2):
            result += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    input_text = request.form['input_text']
    key_value = request.form['key_value']
    cipher_type = request.form['cipher_type']

    if cipher_type == "Caesar":
        shift_value = int(key_value)
        encrypted_text = caesar_cipher(input_text, shift_value)
    elif cipher_type == "Vigenere":
        encrypted_text = vigenere_cipher(input_text, key_value)
    elif cipher_type == "Playfair":
        encrypted_text = playfair_cipher(input_text, key_value)
    else:
        encrypted_text = "Invalid Cipher Type"

    return render_template('index.html', result=f"Encrypted Text: {encrypted_text}")


if __name__ == '__main__':
    app.run(debug=True)

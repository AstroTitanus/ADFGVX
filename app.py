# Importing
from flask import Flask, render_template, request, redirect
from json import loads

# Importing custom libs
from libraries.enums import Mode
from libraries.main import Cipher

# Env setup
app = Flask(__name__)


# Mini helper
def get_missing_data(data_arr, expected_arr):
    missing = []
    for expected_item in expected_arr:
        if expected_item not in data_arr:
            missing.append(f"Oops, {expected_item} seems to be missing.")
    
    return missing

def verify_alphabet_matrix(matrix, expected_size, alphabet_list):
    if len(matrix) != expected_size:
        return "Alphabet matrix has too many rows."

    for row in matrix:
        if len(row) != expected_size:
            return "One or more rows in the alphabet matrix are too big."

        for letter in row:
            if len(letter) > 1:
                return "One or more alphabet matrix cells has more than 1 letter."
    
    # alphabet matrix should only contain alphabet letters
    for row in matrix:
        for letter in row:
            if letter not in alphabet_list:
                return "Alphabet matrix contains an illegal character"

    seen = set()
    duplicates = {}
    for i_index, row in enumerate(matrix):
        for j_index, item in enumerate(row):
            if item in seen:
                duplicates[(i_index, j_index)] = item
            seen.add(item)
    
    if duplicates:
        return "Alphabet matrix has one or more duplicates"
    
    return None




# Flask endpoints
@app.route('/', methods=["GET"])
def main_page():
    if request.method == 'GET':
        return redirect("/encrypt")


@app.route('/encrypt', methods=["GET", "POST"])
def encrypt_web():
    if request.method == 'GET':

        # Default mode
        mode = "ADFGVX"
        if request.args.get("mode"):
            mode = request.args.get("mode")

        if mode == "ADFGX":
            # Language handling
            lang = Mode.SK  # default
            if request.args.get("lang"):
                lang_str = request.args.get("lang").upper()
                lang = Mode.CZ if lang_str == 'CZ' else lang

            # Get random alphabet
            cipher = Cipher("password", lang)
            return render_template("encrypt.html", cipher = cipher)

        else:
            # Get random alphabet
            cipher = Cipher("password", Mode.LONG)
            return render_template("encrypt.html", cipher = cipher)
    
    elif request.method == 'POST':
        # Missing data handling
        missing_data = get_missing_data(request.form.keys(), ['matrix_label', 'password', 'message', 'alphabet_matrix'])
        if missing_data != []:
            cipher = Cipher("password", Mode.LONG)
            return render_template("encrypt.html", errors = missing_data, cipher = cipher)

        matrix_label = request.form['matrix_label']
        password = request.form['password']
        message = request.form['message']
        alphabet_matrix = loads(request.form['alphabet_matrix'])['data']

        if matrix_label == "ADFGX":
            lang = Mode.SK if request.form['lang'] == 'SK' else Mode.CZ
            cipher = Cipher(password, lang)
            cipher.alphabet_matrix = alphabet_matrix

            # Catch errors from constructor
            if cipher.errors:
                return render_template("encrypt.html", errors = cipher.errors, cipher = cipher)

            # Check alphabet size
            error = verify_alphabet_matrix(alphabet_matrix, 5, cipher.alphabet_list)
            if error:
                return render_template("encrypt.html", errors = [error], cipher = cipher)
            
            # Encrypt
            try:
                encrypted = cipher.encrypt(message)
            except:
                return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")

            # Catch errors from encryption
            if cipher.errors:
                return render_template("encrypt.html", errors = cipher.errors, cipher = cipher)

            # Data for template
            cipher_data = {}
            cipher_data['encrypted'] = encrypted
            cipher_data['cipher'] = cipher

            return render_template("encrypt_success.html", data = cipher_data)    

        elif matrix_label == "ADFGVX":
            cipher = Cipher(password, Mode.LONG)
            cipher.alphabet_matrix = alphabet_matrix

            # Catch errors from constructor
            if cipher.errors:
                return render_template("encrypt.html", errors = cipher.errors, cipher = cipher)

            # Check alphabet size
            error = verify_alphabet_matrix(alphabet_matrix, 6, cipher.alphabet_list)
            if error:
                return render_template("encrypt.html", errors = [error], cipher = cipher)
            
            # Encrypt
            try:
                encrypted = cipher.encrypt(message)
            except:
                return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")

            # Catch errors from encryption
            if cipher.errors:
                return render_template("encrypt.html", errors = cipher.errors, cipher = cipher)

            # Data for template
            cipher_data = {}
            cipher_data['encrypted'] = encrypted
            cipher_data['cipher'] = cipher
        
            return render_template("encrypt_success.html", data = cipher_data)

        return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")


@app.route('/decrypt', methods=["GET", "POST"])
def decrypt_web():
    if request.method == 'GET':

        # Default mode
        mode = "ADFGVX"
        if request.args.get("mode"):
            mode = request.args.get("mode")

        alphabet_matrix = None
        if request.args.get("alphabet"):
            alphabet_matrix = loads(request.args.get("alphabet"))

        if mode == "ADFGX":
            # Language handling
            lang = Mode.SK  # default
            if request.args.get("lang"):
                lang_str = request.args.get("lang").upper()
                lang = Mode.CZ if lang_str == 'CZ' else lang

            # Get cipher object
            cipher = Cipher("password", lang)

            # Set cipher alphabet if alphabet is sent in get request
            if alphabet_matrix:
                error = verify_alphabet_matrix(alphabet_matrix, 5, cipher.alphabet_list)
                if error:
                    return render_template("decrypt.html", errors = [error], cipher = cipher)
                cipher.alphabet_matrix = alphabet_matrix

            return render_template("decrypt.html", cipher = cipher)

        else:
            # Get cipher object
            cipher = Cipher("password", Mode.LONG)

            # Set cipher alphabet if alphabet is sent in get request
            if alphabet_matrix:
                error = verify_alphabet_matrix(alphabet_matrix, 6, cipher.alphabet_list)
                if error:
                    return render_template("decrypt.html", errors = [error], cipher = cipher)
                cipher.alphabet_matrix = alphabet_matrix

            return render_template("decrypt.html", cipher = cipher)
    
    elif request.method == 'POST':
        # Missing data handling
        missing_data = get_missing_data(request.form.keys(), ['matrix_label', 'password', 'message', 'alphabet_matrix'])
        if missing_data != []:
            cipher = Cipher("password", Mode.LONG)
            return render_template("decrypt.html", errors = missing_data, cipher = cipher)

        matrix_label = request.form['matrix_label']
        password = request.form['password']
        message = request.form['message']
        alphabet_matrix = loads(request.form['alphabet_matrix'])['data']

        if matrix_label == "ADFGX":
            lang = Mode.SK if request.form['lang'] == 'SK' else Mode.CZ
            cipher = Cipher(password, lang)
            cipher.alphabet_matrix = alphabet_matrix

            # Catch errors from constructor
            if cipher.errors:
                return render_template("decrypt.html", errors = cipher.errors, cipher = cipher)

            # Check alphabet size
            error = verify_alphabet_matrix(alphabet_matrix, 5, cipher.alphabet_list)
            if error:
                return render_template("decrypt.html", errors = [error], cipher = cipher)
            
            # Decrypt
            try:
                decrypted = cipher.decrypt(message)
            except:
                return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")

            # Catch errors from decryption
            if cipher.errors:
                return render_template("decrypt.html", errors = cipher.errors, cipher = cipher)

            # Data for template
            cipher_data = {}
            cipher_data['decrypted'] = decrypted
            cipher_data['cipher'] = cipher

            return render_template("decrypt_success.html", data = cipher_data)    

        elif matrix_label == "ADFGVX":
            cipher = Cipher(password, Mode.LONG)
            cipher.alphabet_matrix = alphabet_matrix

            # Catch errors from constructor
            if cipher.errors:
                return render_template("decrypt.html", errors = cipher.errors, cipher = cipher)

            # Check alphabet size
            error = verify_alphabet_matrix(alphabet_matrix, 6, cipher.alphabet_list)
            if error:
                return render_template("decrypt.html", errors = [error], cipher = cipher)
            
            # Decrypt
            try:
                decrypted = cipher.decrypt(message)
            except:
                return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")

            # Catch errors from decryption
            if cipher.errors:
                return render_template("decrypt.html", errors = cipher.errors, cipher = cipher)

            # Data for template
            cipher_data = {}
            cipher_data['decrypted'] = decrypted
            cipher_data['cipher'] = cipher
        
            return render_template("decrypt_success.html", data = cipher_data)

        return render_template("error.html", error_message = "Oops, this wasn't supposed to happen. Try again.")


if __name__ == "__main__":
    app.run()
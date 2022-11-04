from libraries.enums import Mode, Type
import libraries.helper as h

class Cipher():
        
    def __init__(self, plain_password, mode):
        self.errors = []

        if not mode:
            self.errors.append("Jazyk musi byt zvoleny")

        if len(h.clean_string(plain_password, Type.PASSWORD, h.get_alphabet_list(mode), mode)) < 5:
            self.errors.append("Heslo musi obsahovat minimalne 5 unikatnych pismen.")

        self.plain_password = plain_password
        self.mode = mode
        self.alphabet_list = h.get_alphabet_list(mode)
        self.alphabet_matrix_size = 5 if mode == Mode.SK or mode == Mode.CZ else 6
        self.alphabet_matrix_label = "ADFGX" if mode == Mode.SK or mode == Mode.CZ else "ADFGVX"
        self.alphabet_matrix = h.random_alphabet_matrix(self.alphabet_list, self.alphabet_matrix_size)
        self.encrypted_matrix = None
        self.clean_password = h.clean_string(self.plain_password, Type.PASSWORD, self.alphabet_list, self.mode)
        self.sorted_clean_password = sorted(list(self.clean_password))
    

    def encrypt(self, plain_input):
        # Password cleaning
        clean_password = h.clean_string(self.plain_password, Type.PASSWORD, self.alphabet_list, self.mode)

        # Text input cleaning
        try:
            encoded_text = h.encode_text(plain_input, self.mode)
        except Exception as e:
            self.errors.append(e.args[0])
            return
        clean_text = h.clean_string(encoded_text, Type.ENCRYPT, self.alphabet_list, self.mode)

        if clean_text == "":
            self.errors.append("Text to encrypt can't be empty.")
            return

        # Encode letters to coordinates string
        coord_string = ""
        for letter in clean_text:
            try:
                row, col = h.find_letter_coordinates(self.alphabet_matrix, letter)
            except Exception as e:
                self.errors.append(e.args[0])
                return
                
            coord_string += self.alphabet_matrix_label[row] + self.alphabet_matrix_label[col]
        
        # Add spaces for correct decryption
        if len(coord_string) % len(clean_password) != 0:
            mod = len(coord_string) % len(clean_password)
            spaces_to_add = len(clean_password) - mod
            coord_string += spaces_to_add * " "        

        # Convert coordinates string to encrypted string
        sorted_password_list = sorted(list(clean_password))
        clean_password_list = list(clean_password)

        encrypted_string = ""
        for char in sorted_password_list:
            col_index = clean_password_list.index(char)
            encrypted_string += "".join([letter for i, letter in enumerate(coord_string) if i % len(clean_password) == col_index])
        
        # Generate encrypted matrix from encrypted string
        encrypted_cols = [item for item in h.split_to_groups(encrypted_string, int(len(encrypted_string) / len(clean_password)), 'list')]
        encrypted_matrix = []
        for i in range(2):
            encrypted_matrix.append([item[i] for item in encrypted_cols])
        self.encrypted_matrix = encrypted_matrix

        return encrypted_string
    
    
    def decrypt(self, encrypted_input):
        # Cleaning
        clean_password = h.clean_string(self.plain_password, Type.PASSWORD, self.alphabet_list, self.mode)
        clean_encrypted = h.clean_string(encrypted_input, Type.DECRYPT, self.alphabet_list, self.mode)

        # Invalid encrypted inputs
        if not set(clean_encrypted.replace(" ", "")).issubset(set(self.alphabet_matrix_label)):
            self.errors.append(f"Encrypted input can contain letters '{self.alphabet_matrix_label}' only.")
            return
        
        if len(clean_password) > len(clean_encrypted):
            self.errors.append("Encrypted input can't be shorter than password")
            return
        
        sorted_password_list = sorted(list(clean_password))
        clean_password_list = list(clean_password)

        # Split to columns (password matrix)
        groups_length = int(len(clean_encrypted) / len(clean_password))
        sorted_passw_cols = h.split_to_groups(clean_encrypted, groups_length, "list")

        # Generate encrypted matrix from encrypted string
        encrypted_matrix = []
        for i in range(2):
            encrypted_matrix.append([item[i] for item in sorted_passw_cols])
        self.encrypted_matrix = encrypted_matrix

        # Sort columns into the right order according to password
        passw_cols = [[] for arr in range(len(clean_password))]
        for i, char in enumerate(sorted_password_list):
            col_index = clean_password_list.index(char)
            passw_cols[col_index] = sorted_passw_cols[i]

        # Get coordinates in string
        coordinates_string = ""
        for i in range(groups_length):
            for col in passw_cols:
                coordinates_string += col[i]    
        coordinates_string = coordinates_string.replace(" ", "")

        # Get encoded text from coordinates
        encoded_text = ""
        coord_letter_pairs = h.split_to_groups(coordinates_string, 2, "list")
        for coord_letter_pair in coord_letter_pairs:
            try:
                encoded_text += h.get_letter(self.alphabet_matrix, self.alphabet_matrix_label, coord_letter_pair)
            except:
                self.errors.append("Invalid encrypted input.")
                return
        
        # Decode
        try:
            decoded = h.decode_text(encoded_text, self.mode)
        except Exception as e:
            self.errors.append(e.args[0])
            return

        return decoded
#--------------------#
#  HELPER FUNCTIONS  #
#--------------------#

# Env imports
from json import loads
import unidecode
from string import ascii_uppercase, digits
from random import shuffle
from copy import deepcopy

# Local imports
from libraries.enums import Mode, Type


def get_alphabet_list(mode):
    if mode == Mode.SK:
        return list(ascii_uppercase.replace("V", ""))

    elif mode == Mode.CZ:
        return list(ascii_uppercase.replace("Q", ""))

    else:
        return list(ascii_uppercase + digits)


# TODO: ASI DELETE - ZATIAL NIE JE USED (bolo pouzite v constructore)
def password_validity(cipher):
    clean_pass = clean_string(cipher.plain_password, Type.PASSWORD, cipher.alphabet_list, cipher.mode)
    
    if len(clean_pass) < 5:
        return False

    return True


def random_alphabet_matrix(alphabet_list, alphabet_matrix_size):
    alphabet_matrix = []
    random_alphabet = deepcopy(alphabet_list)

    # Shuffles list in argument
    shuffle(random_alphabet)

    # Slice list to rows for alphabet matrix
    rows = split_to_groups(random_alphabet, alphabet_matrix_size, "list")

    # Fill matrix with shuffled alphabet
    for i in range(alphabet_matrix_size):
        alphabet_matrix.append(rows[i])
    
    return alphabet_matrix


def get_letter(alphabet_matrix, alphabet_matrix_label, coord_letter_group):
    row = alphabet_matrix_label.index(coord_letter_group[0])
    col = alphabet_matrix_label.index(coord_letter_group[1])
    
    return alphabet_matrix[row][col]


def find_letter_coordinates(alphabet_matrix, letter):
    for i, row in enumerate(alphabet_matrix):
        for j, item in enumerate(row):
            if item == letter:
                return i, j

    raise Exception(f"Letter '{letter}' not found in the alphabet")


def pretty_matrix(matrix):
    result = ""

    for i, row in enumerate(matrix):
        if i == len(matrix) - 1:
            result += ' '.join(row)
        else:
            result += ' '.join(row) + "\n"
    
    return result


def clean_string(str, type, alphabet_list, mode):
    # Remove all accents
    str_unaccented = unidecode.unidecode(str)

    # Convert to uppercase
    clean_string = str_unaccented.upper()

    # Replace one character based on language
    if mode == Mode.SK:
        clean_string = clean_string.replace("V", "F")
    elif mode == Mode.CZ:
        clean_string = clean_string.replace("Q", "K")

    # Filter all non-alphabet except characters
    clean_string = "".join([char for char in clean_string if char in alphabet_list or char == " "])

    # Special cases
    if type == Type.PASSWORD:
        # No spaces allowed in the password?
        clean_string = clean_string.replace(" ", "")
        
        # Remove all duplicates from password
        clean_string = "".join(dict.fromkeys(clean_string))
        
    return clean_string


def split_to_groups(data, group_len, return_type):
    if return_type == "str":
        return "".join([data[i:i+group_len] for i in range(0, len(data), group_len)])
    else:
        return [data[i:i+group_len] for i in range(0, len(data), group_len)]


def get_encode_dict(type):
    data = None

    try:
        with open("libraries/encode_dictionary.json", "r") as f:
            data = f.read()
    except:
        raise Exception("An error occured while oppening encode dictionary file.")
    
    data_dict = loads(data)
    return data_dict[type]


def decode_text(text, mode):
    decoded_text = text

    # Special character
    try:
        encode_dict = get_encode_dict("special_chars")
    except Exception as e:
        raise e
    
        # Decoding
    for plain, encoded in encode_dict.items():
        decoded_text = decoded_text.replace(encoded, plain)

    if mode == Mode.SK or mode == Mode.CZ:
        # Numbers
        try:
            encode_dict = get_encode_dict("numbers")
        except Exception as e:
            raise e

            # Decoding
        for plain, encoded in encode_dict.items():
            decoded_text = decoded_text.replace(encoded, plain)
               
    return decoded_text


def encode_text(text, mode):
    encoded_text = text

    # Special characters
    try:
        encode_dict = get_encode_dict("special_chars")
    except Exception as e:
        raise e
    
        # Encoding
    for plain, encoded in encode_dict.items():
        encoded_text = encoded_text.replace(plain, encoded)

    if mode == Mode.SK or mode == Mode.CZ:
        # Numbers
        try:
            encode_dict = get_encode_dict("numbers")
        except Exception as e:
            raise e

            # Encoding
        for plain, encoded in encode_dict.items():
            encoded_text = encoded_text.replace(plain, encoded)
               
    return encoded_text
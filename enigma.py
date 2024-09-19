'''
Author: Felice Angie Chandra
SBUID: 115343711
CLASS: CSE360

'''

class EnigmaMachine:
    """
    In this assignment, we will implement the Enigma Machine. 
    
    Example input:
    Input:
    B123AAA
    AB,CD,EF
    SECURITY

    Output:
    JKJRFLHF

    Input:
        reflector_code (str): The code of the reflector (A/B/C)
        rotors (str): A 3-character string representing the numbers for three rotors (1-5).
        rotor_pos (str): A 3-character string representing the rotor starting positions (A-Z).
        plugboard_setup (str): A comma-separated string of plugboard pairs (no duplicates/empty).
        message (str): The message to be encrypted (A-Z).

    Output:
        The encrypted message as a string (A-Z).
    """
    def __init__(self, reflector_code, rotor_codes, rotor_pos, plugboard_pairs):
        # The internal wiring of each rotor (1-5) and notch locations
        self.rotors = {
            '1': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
            '2': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
            '3': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
            '4': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
            '5': ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
        }
        
        # Reflector wiring for A, B, and C
        self.reflectors = {
            'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
            'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
        }
        
        # Set initial positions
        self.rotor_pos = [ord(pos) - ord('A') for pos in rotor_pos]
        
        # Plugboard settings
        self.plugboard = self.create_plugboard(plugboard_pairs)
        
        # Initialize selected rotors and reflector
        self.reflector = self.reflectors[reflector_code]
        self.rotor_sequence = [self.rotors[rotor_codes[i]][0] for i in range(3)]
        self.notch_pos = [self.rotors[rotor_codes[i]][1] for i in range(3)]
       
    def create_plugboard(self, pairs):
        # Set up plugboard with character swaps
        plugboard = {}
        for pair in pairs.split(','):
            if len(pair) == 2:
                plugboard[pair[0]] = pair[1]
                plugboard[pair[1]] = pair[0]
        return plugboard
    
    def plugboard_swap(self, char):
        return self.plugboard.get(char, char)

    def rotate_rotors(self):
        # Rotate the rightmost rotor will always step
        # Check if middle rotor needs to step
        # if the rightmost rotor is in its notch position,
        # it rotates the middle rotor
        self.rotor_pos[2] = (self.rotor_pos[2] + 1) % 26
        
        if chr(self.rotor_pos[2] + ord('A')) == self.notch_pos[2]:
            self.rotor_pos[1] = (self.rotor_pos[1] + 1) % 26
            if chr(self.rotor_pos[1] + ord('A')) == self.notch_pos[1]:
                self.rotor_pos[0] = (self.rotor_pos[0] + 1) % 26
        
        # Right rotor always steps every keypress
        right_notch_reached = chr(self.rotor_pos[2] + ord('A')) == self.notch_pos[2]
        self.rotor_pos[2] = (self.rotor_pos[2] + 1) % 26
        
        # If right rotor was at notch position, rotate middle rotor
        if right_notch_reached:
            middle_notch_reached = chr(self.rotor_pos[1] + ord('A')) == self.notch_pos[1]
            self.rotor_pos[1] = (self.rotor_pos[1] + 1) % 26
            
            # If middle rotor was at notch position, rotate left rotor
            if middle_notch_reached:
                self.rotor_pos[0] = (self.rotor_pos[0] + 1) % 26

            # print(f"Rotors Position: {''.join([chr(pos + ord('A')) for pos in self.rotor_pos])}")
        

    def encrypt_character(self, char):
        # Rotate rotors with every key press
        self.rotate_rotors()
        
        # Pass through plugboard
        initial_char = char
        char = self.plugboard_swap(char)
        # print(f"Pass into plugboard: {initial_char} -> {char}")
        
        # Pass through rotors (right to left)
        for i in range(2, -1, -1):
            input_char = char
            char = chr(((ord(char) - ord('A') + self.rotor_pos[i]) % 26) + ord('A'))
            char = self.rotor_sequence[i][ord(char) - ord('A')]
            char = chr((ord(char) - ord('A') - self.rotor_pos[i]) % 26 + ord('A'))
            # print(f"Rotated back rotor {i+1} is from {input_char} to {char}")
        
        # Pass through reflector
        input_char = char
        char = self.reflector[ord(char) - ord('A')]
        # print(f"After going through reflector: {input_char} -> {char}")
        
        # Pass back through rotors (left to right)
        for i in range(3):
            input_char = char
            char = chr(((ord(char) - ord('A') + self.rotor_pos[i]) % 26) + ord('A'))
            char = chr(self.rotor_sequence[i].index(char) + ord('A'))
            char = chr((ord(char) - ord('A') - self.rotor_pos[i]) % 26 + ord('A'))
            # print(f"Rotated rotor {i+1} is from {input_char} to {char}")
        
        # Pass through plugboard again
        final_char = char
        char = self.plugboard_swap(char)
        # print(f"Pass into plugboard again: {final_char} -> {char}\n\n")
        
        return char
    
    def encrypt_message(self, message):
            result = []
            for char in message:
                if char.isalpha():
                    result.append(self.encrypt_character(char.upper()))
            return ''.join(result)


# this is where we parse the input
def main():

    # ask user for input (3 lines)
    # print("Enter the input:")
    rotor_setup = input()
    plugboard_setup = input()
    message = input()
    
    # parsing the first line input
    reflector_code = rotor_setup[0]
    rotors = rotor_setup[1:4]
    rotor_pos = rotor_setup[4:7]
    
    enigma = EnigmaMachine(reflector_code, rotors, rotor_pos, plugboard_setup)
    
    # encrypt the message
    # print("\nOutput:")
    output = enigma.encrypt_message(message)
    print(output)

def test_enigma():

    firstline = 'B123AAA'
    secondline = 'AB,CD,EF'
    
    a = firstline[0]
    b = firstline[1:4]
    c = firstline[4:7]

    print(f"Current settings:\n{a}{b}{c}\n{secondline}")
    
    enigma = EnigmaMachine(a, b, c, secondline)
    
    print("\ninitial rotor positions:")
    print([chr(pos + ord('A')) for pos in enigma.rotor_pos])
    
    print("\nplugboard setting:")
    test_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for char in test_chars:
        swapped_char = enigma.plugboard_swap(char)
        print(f"{char} -> {swapped_char}")

    # for i in range(5): # will rotate rightmost rotor 5 times
    #     enigma.rotate_rotors()
    #     print(f"Rotor positions after rotation {i+1}: {[chr(pos + ord('A')) for pos in enigma.rotor_pos]}")
    
    test_chars = 'HELLO'
    output = enigma.encrypt_message(test_chars)
    print(f"encrypted message: {output}")


if __name__ == '__main__':
    main()
    # test_enigma()

import string
import random
from copy import deepcopy

ALPHABET = string.ascii_uppercase

def rotate_rotor(rotor):
    return rotor[1:] + rotor[0]

def create_rotor():
    shuffled = list(ALPHABET)
    random.shuffle(shuffled)
    return ''.join(shuffled)

class FialkaSimulator:
    def __init__(self, rotors=None, reflector=None, plugboard=None):
        self.rotors = deepcopy(rotors) if rotors else [create_rotor() for _ in range(10)]
        self.rotor_positions = [0] * 10
        self.reflector = deepcopy(reflector) if reflector else self.create_reflector()
        self.plugboard = deepcopy(plugboard) if plugboard else self.create_plugboard()

    def create_reflector(self):
        letters = list(ALPHABET)
        random.shuffle(letters)
        reflector = {}
        for i in range(0, len(letters), 2):
            a, b = letters[i], letters[i+1]
            reflector[a] = b
            reflector[b] = a
        return reflector

    def create_plugboard(self):
        wiring = {c: c for c in ALPHABET}
        pairs = random.sample(ALPHABET, 20)  # 10 random swaps
        for i in range(0, 20, 2):
            a, b = pairs[i], pairs[i+1]
            wiring[a], wiring[b] = b, a
        return wiring

    def step_rotors(self):
        for i in range(10):
            self.rotors[i] = rotate_rotor(self.rotors[i])
            self.rotor_positions[i] = (self.rotor_positions[i] + 1) % 26
            if self.rotor_positions[i] != 0:
                break

    def encrypt_letter(self, ch):
        if ch not in ALPHABET:
            return ch
        
        self.step_rotors()
        ch = self.plugboard[ch]

        for rotor in self.rotors:
            index = ALPHABET.index(ch)
            ch = rotor[index]

        ch = self.reflector.get(ch, ch)

        for rotor in reversed(self.rotors):
            index = rotor.index(ch)
            ch = ALPHABET[index]

        ch = self.plugboard[ch]
        return ch

    def encrypt(self, text):
        text = text.upper()
        return ''.join(self.encrypt_letter(ch) for ch in text if ch in ALPHABET)

def main():
    # Initialize machine and save starting state
    simulator = FialkaSimulator()
    initial_rotors = deepcopy(simulator.rotors)
    initial_reflector = deepcopy(simulator.reflector)
    initial_plugboard = deepcopy(simulator.plugboard)

    while True:
        choice = input("\nChoose (E)ncrypt, (D)ecrypt or (Q)uit: ").strip().upper()
        if choice == 'Q':
            print("Goodbye!")
            break
        elif choice not in ('E', 'D'):
            print("Please choose E, D, or Q.")
            continue

        text = input("Enter text (letters A-Z only): ").strip().upper()

        # Reset machine to initial state before each operation
        simulator = FialkaSimulator(
            rotors=initial_rotors,
            reflector=initial_reflector,
            plugboard=initial_plugboard
        )
        simulator.rotor_positions = [0] * 10

        if choice == 'E':
            result = simulator.encrypt(text)
            print("Encrypted text:", result)
        else:
            # Decryption is same as encryption with same settings
            result = simulator.encrypt(text)
            print("Decrypted text:", result)

if __name__ == "__main__":
    main()

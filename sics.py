from collections import Counter

class SICS:
    def __init__(self):
        self.char_to_code = {}
        self.code_to_char = {}

    def _generate_codes(self, sorted_chars):
        def hex_code_generator():
            length = 1
            while True:
                for i in range(16 ** length):
                    hex_str = f"{i:0{length}X}"
                    if all(c == 'F' for c in hex_str[:-1]) and hex_str[-1] != 'F':
                        yield hex_str
                length += 1

        gen = hex_code_generator()
        for char in sorted_chars:
            code = next(gen)
            self.char_to_code[char] = code
            self.code_to_char[code] = char

    def compress(self, message):
        freq = Counter(message)
        sorted_chars = [char for char, _ in freq.most_common()]
        self._generate_codes(sorted_chars)

        result = ""
        for char in message:
            result += self.char_to_code[char]
        return result

    def decompress(self, compressed):
        result = ""
        idx = 0
        while idx < len(compressed):
            # Read until a non-'F' nibble
            start = idx
            while compressed[idx] == 'F':
                idx += 1
            idx += 1
            code = compressed[start:idx]
            char = self.code_to_char.get(code)
            if char is None:
                raise ValueError(f"Invalid code: {code}")
            result += char
        return result

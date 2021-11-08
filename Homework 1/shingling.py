import binascii

class Shingling: 

    def __init__(self, text: str, k: int):
        self.shingles = set()
        text = text.lower()
        for i in range(len(text)+1-k):
            shingle = text[i:i+k]
            # Hash the shingle to a 32-bit integer.
            hashed_value = binascii.crc32(bytes(shingle, 'utf-8')) & 0xffffffff
            #hashed_value = shingle
            self.shingles.add(hashed_value)
        self.shingles = sorted(self.shingles)

# example usage
#s = Shingling("abcab", 2)
#print(s.shingles)
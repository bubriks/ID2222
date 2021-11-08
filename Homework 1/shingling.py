class Shingling:

    def __init__(self, text: str, k: int):
        self.shingles = set()
        text = text.lower()
        for i in range(len(text)+1-k):
            hashed_value = hash(text[i:i+k])
            self.shingles.add(hashed_value)
        self.shingles = sorted(self.shingles)

# example usage
s = Shingling("abcab", 2)
print(s.shingles)
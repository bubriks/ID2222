class Shingling: 

    def __init__(self, text: str, k: int):
        self.shingles = set()
        text = text.lower()
        for i in range(len(text)+1-k):
            shingle = text[i:i+k]
            self.shingles.add(shingle)

    @staticmethod
    def get_vocabs(shingles_df):
        return set().union(*shingles_df["data"].tolist())

    @staticmethod
    def one_hot_encoder(shingles_df, vocabs):
        shingles_df["data"] = shingles_df.apply(lambda row: [1 if i in row["data"] else 0 for i in vocabs], axis=1)


# # example usage
# s = Shingling("abcab", 2)
# print(s.binary_singles)
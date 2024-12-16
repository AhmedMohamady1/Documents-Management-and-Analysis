from collections import Counter
from math import*

class SimilarityGetter:

    def __init__(self, texts: list):
        tokenized_texts = [text.lower().split() for text in texts]
        self.vocabulary = set(word for text in tokenized_texts for word in text)
        self.bow_vectors = []
        for text in tokenized_texts:
            word_count = Counter(text)
            vector = [word_count.get(word, 0) for word in self.vocabulary]
            self.bow_vectors.append(vector)

    def square_rooted(self, vector):
        return round(sqrt(sum([x * x for x in vector])), 3)

    def cosine_similarity(self):
        numerator = sum(x * y for x, y in zip(self.bow_vectors[0], self.bow_vectors[1]))
        denominator = self.square_rooted(self.bow_vectors[0]) * self.square_rooted(self.bow_vectors[1])
        return round(numerator/float(denominator), 3)

    def jaccard_similarity(self):
        set1 = set(i for i, v in enumerate(self.bow_vectors[0]) if v > 0)
        set2 = set(i for i, v in enumerate(self.bow_vectors[1]) if v > 0)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union != 0 else 0

    def euclidean_distance(self):
        return round((sqrt(sum(pow(x - y, 2) for x, y in zip(self.bow_vectors[0], self.bow_vectors[1])))), 3)

texts = [
    "The greenhouse controls temperature and humidity levels automatically Sensors measure soil moisture air quality and light intensity precisely",
    "Humidity and temperature impact soil conditions Greenhouse sensors monitor light air quality and moisture for efficient plant growth"
]

similarity_test = SimilarityGetter(texts)
print(similarity_test.cosine_similarity())
print(similarity_test.jaccard_similarity())
print(similarity_test.euclidean_distance())
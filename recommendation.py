import numpy as np
import json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("./data/fonts.json", "r") as file:
    fonts = json.load(file)

def recommend_ranks(query, limit=10):

    model = SentenceTransformer('all-MiniLM-L6-v2')

    font_descriptions = [font["description"] for font in fonts.values()]

    font_embeddings = model.encode(font_descriptions, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(query_embedding, font_embeddings).flatten().tolist()

    ranked_fonts = sorted(
        zip(fonts.items(), similarity_scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [{"name": font[0], "details": font[1], "score": score} for (font, score) in ranked_fonts[:limit]]
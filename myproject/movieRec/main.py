import os
import pandas as pd
import json
import numpy as np

# Get the directory of this file (main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load precomputed neighbors from JSON using an absolute path
json_path = os.path.join(BASE_DIR, "top10_neighbors.json")
with open(json_path, "r", encoding="utf-8") as f:
    top_neighbors = json.load(f)

def recommend_for_user(liked_movies, top_neighbors, top_n=3):
    scores = {}

    # Go through each liked movie
    for movie in liked_movies:
        if movie not in top_neighbors:
            continue 
        for neighbor in top_neighbors[movie]:
            title = neighbor["title"]
            sim = neighbor["similarity"]
            
            if title not in liked_movies:  
                scores[title] = scores.get(title, 0) + sim
    print(scores)

    # Average the score across liked movies
    if liked_movies:
        for k in scores:
            scores[k] /= len(liked_movies)

    # Convert to DataFrame for sorting
    results = pd.DataFrame(scores.items(), columns=["title", "score"])
    results = results.sort_values("score", ascending=False).head(top_n)
    
    return results

# Example usage
print(recommend_for_user(
    ["Toy Story (1995)", "Jumanji (1995)"],  
    top_neighbors,
    top_n=5
))

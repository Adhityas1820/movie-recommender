import pandas as pd
from sklearn.neighbors import NearestNeighbors
import json
import os

# Load movies
movies = pd.read_csv("movie-rec-algorithm/movies.csv")
pd.set_option("display.max_columns", None)   
pd.set_option("display.width", None)        

print(movies.head(20)) 

# Create feature matrix from genres
feature_matrix = movies['genres'].str.get_dummies('|')
print(feature_matrix.head(20))  # shows first 20 rows with genre columns

# Fit NearestNeighbors model
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(feature_matrix)

distances, indices = nn.kneighbors(feature_matrix, n_neighbors=10)

# Build dictionary for JSON
top_neighbors = {}

for i, movie_id in enumerate(movies['movieId']):
    neighbors = []
    for j, idx in enumerate(indices[i]):
        if idx == i:
            continue  # skip itself
        neighbors.append({
            "title": movies.iloc[idx]['title'],
            "genres": movies.iloc[idx]['genres'],
            "similarity": float(1 - distances[i][j])  # convert numpy.float -> normal float
        })
    top_neighbors[movies.iloc[i]['title']] = neighbors

# Path to save JSON
output_path = os.path.join("movie-rec-algorithm", "top10_neighbors.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(top_neighbors, f, indent=2, ensure_ascii=False)

print("Saved top 10 neighbors for each movie into top10_neighbors.json")




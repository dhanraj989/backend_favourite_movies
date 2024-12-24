from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

FAVORITES_FILE = "favorites.json"

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load favorites from the JSON file
def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save favorites to the JSON file
def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as file:
        json.dump(favorites, file)

@app.get("/favorites")
def get_favorites():
    return load_favorites()

@app.post("/favorites")
def add_favorite(favorite: dict):
    favorites = load_favorites()
    favorites.append(favorite)
    save_favorites(favorites)
    return {"message": "Favorite added successfully!"}

@app.delete("/favorites/{id}")
def delete_favorite(id: str):
    favorites = load_favorites()
    favorites = [f for f in favorites if f["id"] != id]
    save_favorites(favorites)
    return {"message": "Favorite removed successfully!"}

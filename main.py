import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# File to store favorites
FAVORITES_FILE = "favorites.json"

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
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

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Favorites API!"}

# Get all favorites
@app.get("/favorites")
def get_favorites():
    return load_favorites()

# Add a new favorite
@app.post("/favorites")
def add_favorite(favorite: dict):
    favorites = load_favorites()
    favorites.append(favorite)
    save_favorites(favorites)
    return {"message": "Favorite added successfully!"}

# Remove a favorite by ID
@app.delete("/favorites/{id}")
def delete_favorite(id: str):
    favorites = load_favorites()
    updated_favorites = [f for f in favorites if f["id"] != id]
    if len(favorites) == len(updated_favorites):
        raise HTTPException(status_code=404, detail="Favorite not found")
    save_favorites(updated_favorites)
    return {"message": "Favorite removed successfully!"}

# Entry point for Render or local development
if __name__ == "__main__":
    # Use PORT environment variable for deployment, default to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

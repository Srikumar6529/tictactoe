from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from ai import best_move

app = FastAPI()

# 1. Mount the frontend directory
# This makes everything in /frontend available at your URL
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 2. Serve the index.html at the root URL
@app.get("/")
async def read_index():
    return FileResponse(os.path.join("frontend", "index.html"))

# IMPORTANT: This allows your HTML/JS file to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the board data looks like
class BoardState(BaseModel):
    board: list[str]

@app.post("/get-move")
async def get_move(data: BoardState):
    board = data.board
    
    # Logic: Find empty spots
    empty_indices = [i for i, val in enumerate(board) if val == ""]
    
    if not empty_indices:
        return {"move": None, "status": "draw"}

    # Computer picks a move
    computer_move = best_move(board)
    return {"move": computer_move}
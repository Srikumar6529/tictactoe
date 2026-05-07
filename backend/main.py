from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

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
    computer_move = random.choice(empty_indices)
    return {"move": computer_move}
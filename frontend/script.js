let currentPlayer = "X";
let gameActive = true;
let gameState = ["", "", "", "", "", "", "", "", ""];
let isMachineThinking = false; // Prevents clicking while AI is moving

const winningConditions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

const cells = document.querySelectorAll('.cell');
const statusDisplay = document.querySelector("#status");

cells.forEach((cell, index) => {
    cell.addEventListener('click', async () => {
        // Stop if cell taken, game over, or waiting for Python
        if (gameState[index] !== "" || !gameActive || isMachineThinking) return;

        // 1. Process User Move (X)
        handleMove(index, cell);

        // 2. If game is still active, ask Python for O's move
        if (gameActive && currentPlayer === "O") {
            await getPythonMove();
        }
    });
});

function handleMove(index, cell) {
    gameState[index] = currentPlayer;
    cell.textContent = currentPlayer;
    cell.style.backgroundColor = currentPlayer === "X" ? "orange" : "red";
    
    checkResult();
}

async function getPythonMove() {
    isMachineThinking = true;
    statusDisplay.textContent = "AI is thinking...";

    try {
        const response = await fetch('http://127.0.0.1:8000/get-move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board: gameState })
        });

        const data = await response.json();

        if (data.move !== null && gameActive) {
            const aiIndex = data.move;
            const aiCell = cells[aiIndex];
            handleMove(aiIndex, aiCell);
        }
    } catch (error) {
        console.error("Connection to FastAPI failed:", error);
        statusDisplay.textContent = "Error: Backend Offline";
    } finally {
        isMachineThinking = false;
    }
}

function checkResult() {
    let roundWon = false;

    for (let i = 0; i < winningConditions.length; i++) {
        const [a, b, c] = winningConditions[i];
        if (gameState[a] === "" || gameState[b] === "" || gameState[c] === "") continue;
        if (gameState[a] === gameState[b] && gameState[b] === gameState[c]) {
            [a, b, c].forEach(idx => cells[idx].style.backgroundColor = "#2ecc71");
            roundWon = true;
            break;
        }
    }

    if (roundWon) {
        statusDisplay.textContent = `Player ${currentPlayer} Wins!`;
        gameActive = false;
        return;
    }

    if (!gameState.includes("")) {
        statusDisplay.textContent = "It's a draw!";
        gameActive = false;
        return;
    }

    // Switch player
    currentPlayer = currentPlayer === "X" ? "O" : "X";
    statusDisplay.textContent = `Player ${currentPlayer}'s Turn`;
}

document.querySelector('#reset').addEventListener('click', () => {
    currentPlayer = "X";
    gameActive = true;
    isMachineThinking = false;
    gameState = ["", "", "", "", "", "", "", "", ""];
    cells.forEach(cell => {
        cell.textContent = "";
        cell.style.backgroundColor = "white";
    });
    statusDisplay.textContent = "Player X's Turn";
});
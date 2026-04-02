const BOARD_WIDTH = 5; // All words are 5 letters

let currentAnimal;
let currentWord;
let fact;

let attempts = 0;
let maxAttempts = 6;

let score = 0;
let streak = 0;

let currentGuess = "";
let isRevealing = false;

function newWord() {
    currentAnimal = animals[Math.floor(Math.random() * animals.length)];
    currentWord = currentAnimal.word;
    fact = currentAnimal.fact;

    attempts = 0;
    currentGuess = "";
    isRevealing = false;

    document.getElementById("fact").innerText = "";
    document.getElementById("message").innerText = "";

    resetKeyboard();
    createBoard();
}

function createBoard() {
    let board = document.getElementById("board");
    board.innerHTML = "";
    board.style.gridTemplateColumns = `repeat(${BOARD_WIDTH}, 55px)`;

    for (let i = 0; i < BOARD_WIDTH * maxAttempts; i++) {
        let tile = document.createElement("div");
        tile.classList.add("tile");
        board.appendChild(tile);
    }
}

function createKeyboard() {
    const rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
    let keyboard = document.getElementById("keyboard");
    keyboard.innerHTML = "";

    rows.forEach(row => {
        let div = document.createElement("div");
        row.split("").forEach(letter => {
            let key = document.createElement("button");
            key.textContent = letter;
            key.classList.add("key");
            key.onclick = () => pressKey(letter);
            div.appendChild(key);
        });
        keyboard.appendChild(div);
    });

    let enter = document.createElement("button");
    enter.textContent = "ENTER";
    enter.classList.add("key");
    enter.onclick = submitGuess;
    keyboard.appendChild(enter);

    let back = document.createElement("button");
    back.textContent = "←";
    back.classList.add("key");
    back.onclick = deleteLetter;
    keyboard.appendChild(back);
}

function pressKey(letter) {
    if (isRevealing) return;
    if (currentGuess.length >= currentWord.length) return;
    currentGuess += letter;
    updateTiles();
}

function deleteLetter() {
    if (isRevealing) return;
    currentGuess = currentGuess.slice(0, -1);
    updateTiles();
}

function updateTiles() {
    let tiles = document.querySelectorAll(".tile");
    for (let i = 0; i < currentWord.length; i++) {
        let tileIndex = attempts * BOARD_WIDTH + i;
        tiles[tileIndex].textContent = currentGuess[i] || "";
    }
}

function submitGuess() {
    if (isRevealing) return;
    if (currentGuess.length !== currentWord.length) return;

    isRevealing = true;
    let tiles = document.querySelectorAll(".tile");

    for (let i = 0; i < currentWord.length; i++) {
        setTimeout(() => {
            let tileIndex = attempts * BOARD_WIDTH + i;
            let tile = tiles[tileIndex];
            let letter = currentGuess[i];

            tile.classList.add("flip");

            if (letter === currentWord[i]) {
                tile.classList.add("correct");
                colorKey(letter, "correct");
            } else if (currentWord.includes(letter)) {
                tile.classList.add("present");
                colorKey(letter, "present");
            } else {
                tile.classList.add("absent");
                colorKey(letter, "absent");
            }
        }, i * 300);
    }

    setTimeout(() => {
        attempts++;

        if (currentGuess === currentWord) {
            score++;
            streak++;
            document.getElementById("score").innerText = score;
            document.getElementById("streak").innerText = streak;
            document.getElementById("fact").innerText = fact;

            setTimeout(() => {
                isRevealing = false;
                newWord();
            }, 2000);

            currentGuess = "";
            return;
        }

        if (attempts >= maxAttempts) {
            isRevealing = false;
            gameOver();
            return;
        }

        currentGuess = "";
        isRevealing = false;
    }, currentWord.length * 300);
}

function colorKey(letter, status) {
    document.querySelectorAll(".key").forEach(key => {
        if (key.textContent === letter) {
            key.classList.add(status);
        }
    });
}

function resetKeyboard() {
    document.querySelectorAll(".key").forEach(key => {
        key.classList.remove("correct", "present", "absent");
    });
}

function gameOver() {
    streak = 0;
    document.getElementById("streak").innerText = 0;
    document.getElementById("message").innerText =
        "Game Over! The word was " + currentWord;
}

/* physical keyboard support */
document.addEventListener("keydown", function(event) {
    if (isRevealing) return;

    let key = event.key.toLowerCase();

    if (key === "enter") {
        submitGuess();
        return;
    }

    if (key === "backspace") {
        deleteLetter();
        return;
    }

    if (/^[a-z]$/.test(key)) {
        pressKey(key);
    }
});

createKeyboard();
newWord();
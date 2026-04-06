let currentRiddle = null;
let tries = 0;
let score = 0;

function getRandomRiddle() {
  return riddles[Math.floor(Math.random() * riddles.length)];
}

function loadRiddle() {
  if (!riddles || riddles.length === 0) {
    document.getElementById("riddle-text").innerText = "No riddles found!";
    return;
  }

  currentRiddle = getRandomRiddle();
  tries = 0;

  if (!currentRiddle) {
    document.getElementById("riddle-text").innerText = "Error loading riddle.";
    return;
  }

  document.getElementById("riddle-text").innerText = currentRiddle.riddle;
  document.getElementById("hint-text").innerText = "";
  document.getElementById("result-text").innerText = "";
  document.getElementById("answer-input").value = "";
}

function updateScore() {
  document.getElementById("score-display").innerText = "Score: " + score;
}

function checkAnswer() {
  const input = document.getElementById("answer-input").value
    .toLowerCase()
    .trim();

  if (!input) {
    document.getElementById("result-text").innerText = "Enter an answer!";
    return;
  }

  if (input === currentRiddle.answer.toLowerCase()) {
    score++;
    updateScore();

    document.getElementById("result-text").innerText =
      "Correct! +1 point";

    setTimeout(loadRiddle, 1200);
  } else {
    tries++;

    if (tries < 3) {
      document.getElementById("hint-text").innerText =
        "Hint: " + currentRiddle.hints[tries - 1];
      document.getElementById("result-text").innerText =
        `Wrong! (${tries}/3)`;
    } else {
      document.getElementById("result-text").innerText =
        "Out of tries! Answer: " + currentRiddle.answer;

      setTimeout(loadRiddle, 2000);
    }
  }
}

function nextRiddle() {
  loadRiddle();
}

// Enter key support
document.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    checkAnswer();
  }
});

// Start game
updateScore();
loadRiddle();
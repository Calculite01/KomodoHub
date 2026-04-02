let currentRiddle = null;
let tries = 0;
let score = 0;

function getRandomRiddle() {
  return riddles[Math.floor(Math.random() * riddles.length)];
}

function loadRiddle() {
  currentRiddle = getRandomRiddle();
  tries = 0;

  document.getElementById("riddle").innerText = currentRiddle.riddle;
  document.getElementById("hint").innerText = "";
  document.getElementById("result").innerText = "";
  document.getElementById("answer").value = "";
}

function updateScore() {
  document.getElementById("score").innerText = "Score: " + score;
}

function checkAnswer() {
  const input = document.getElementById("answer").value
    .toLowerCase()
    .trim();

  if (!input) {
    document.getElementById("result").innerText =
      "Enter an answer!";
    return;
  }

  if (input === currentRiddle.answer) {
    score++;
    updateScore();

    document.getElementById("result").innerText =
      "Correct! 🎉 (+1 point)";

    setTimeout(loadRiddle, 1200); // auto next
  } else {
    tries++;

    if (tries < 3) {
      document.getElementById("hint").innerText =
        "Hint: " + currentRiddle.hints[tries - 1];
      document.getElementById("result").innerText =
        `Wrong! (${tries}/3)`;
    } else {
      document.getElementById("result").innerText =
        "Out of tries! Answer: " + currentRiddle.answer;

      setTimeout(loadRiddle, 2000); // move on
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
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Edu-Snake Puzzle", page_icon="📖", layout="centered")

# --- LAYOUT STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: #080711;
    }
    .arcade-title {
        font-family: sans-serif;
        font-weight: 900;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 0px;
        color: #ffaa00;
        text-shadow: 0 0 10px rgba(255, 170, 0, 0.4);
    }
    .arcade-sub {
        font-family: 'Share Tech Mono', monospace;
        color: #8b949e;
        text-align: center;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }
    .mobile-container {
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    </style>
    
    <h1 class='arcade-title'>LEXI-SNAKE</h1>
    <p class='arcade-sub'>HIT WALLS TO TRIGGER VOCABULARY GATE PASSES</p>
""", unsafe_allow_html=True)

# --- GAME ENGINE WITH BUILT-IN HTML VOCAB MODAL ---
vocab_snake_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body {
            background-color: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            overflow: hidden;
            font-family: 'Share Tech Mono', monospace;
            user-select: none;
            -webkit-user-select: none;
        }
        .hud {
            width: 320px;
            display: flex;
            justify-content: space-between;
            color: #fff;
            font-size: 18px;
            margin-bottom: 8px;
        }
        .screen-wrapper {
            position: relative;
            border-radius: 8px;
            border: 2px solid #ffaa00;
        }
        #gameCanvas {
            background-color: #030307;
            display: block;
            width: 320px;
            height: 320px;
        }
        
        /* VOCABULARY MODAL OVERLAY */
        #vocabModal {
            display: none; /* Hidden by default */
            position: absolute;
            top: 0; left: 0; width: 320px; height: 320px;
            background: rgba(10, 9, 22, 0.95);
            box-sizing: border-box;
            padding: 15px;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            z-index: 20;
        }
        .quiz-title {
            color: #ffaa00;
            font-size: 16px;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        .quiz-question {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            min-height: 45px;
        }
        .quiz-options {
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
            width: 100%;
        }
        .option-btn {
            background: #1c1a30;
            border: 1px solid #ffaa00;
            color: #fff;
            padding: 8px;
            border-radius: 6px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 14px;
            cursor: pointer;
        }
        .option-btn:active {
            background: #ffaa00;
            color: #000;
        }

        /* CONTROLS */
        .dpad {
            margin-top: 15px;
            display: grid;
            grid-template-columns: repeat(3, 65px);
            grid-template-rows: repeat(3, 60px);
            gap: 8px;
            justify-content: center;
        }
        .dpad-btn {
            background: #16192b;
            color: #ffaa00;
            border: 2px solid #ffaa00;
            border-radius: 12px;
            font-size: 22px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            -webkit-touch-callout: none; 
        }
        .dpad-btn:active {
            background: #ffaa00;
            color: #000;
        }
        .empty { pointer-events: none; visibility: hidden; }

        .btn-restart {
            margin-top: 10px;
            padding: 8px 20px;
            background: #fff;
            color: #000;
            border: none;
            font-family: 'Share Tech Mono', monospace;
            font-size: 16px;
            font-weight: bold;
            border-radius: 4px;
            display: none;
            z-index: 30;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
</head>
<body>

    <div class="hud">
        <div>SCORE: <span id="score">000</span></div>
        <div>SNAKE: <span id="length" style="color: #ffaa00;">3</span></div>
    </div>

    <div class="screen-wrapper">
        <canvas id="gameCanvas" width="400" height="400"></canvas>
        
        <div id="vocabModal">
            <div class="quiz-title">⚠️ WALL WALL BROKEN! SOLVE TO WRAP:</div>
            <div class="quiz-question" id="quizQuestion">What does "Benevolent" mean?</div>
            <div class="quiz-options" id="quizOptions">
                </div>
        </div>
    </div>
    
    <button id="restartBtn" class="btn-restart" onclick="resetGame()">PLAY AGAIN</button>

    <div class="dpad">
        <div class="empty"></div>
        <div class="dpad-btn" id="padUp">▲</div>
        <div class="empty"></div>
        
        <div class="dpad-btn" id="padLeft">◀</div>
        <div class="empty" style="background:#030307; border-radius:50%; visibility:visible; opacity:0.1; border:1px solid #fff;"></div>
        <div class="dpad-btn" id="padRight">▶</div>
        
        <div class="empty"></div>
        <div class="dpad-btn" id="padDown">▼</div>
        <div class="empty"></div>
    </div>

    <script>
        // --- VOCABULARY DATABASE ---
        const VOCAB_BANK = [
            { q: "Which word means 'very generous or kind'?", a: "Magnanimous", o: ["Magnanimous", "Hostile", "Sparse", "Obsolete"] },
            { q: "What is the definition of 'Ephemeral'?", a: "Short-lived", o: ["Permanent", "Short-lived", "Very heavy", "Frightening"] },
            { q: "Choose the synonym for 'Meticulous':", a: "Careful", o: ["Careful", "Lazy", "Sloppy", "Angry"] },
            { q: "What does the word 'Scrutinize' mean?", a: "Examine closely", o: ["Ignore completely", "Examine closely", "Break apart", "Build up"] },
            { q: "Which word means 'difficult to understand'?", a: "Obscure", o: ["Obscure", "Apparent", "Luminous", "Simple"] }
        ];

        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");
        const lengthElement = document.getElementById("length");
        const restartBtn = document.getElementById("restartBtn");
        const vocabModal = document.getElementById("vocabModal");
        const quizQuestion = document.getElementById("quizQuestion");
        const quizOptions = document.getElementById("quizOptions");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        let snake = [{x: 10, y: 10}, {x: 9, y: 10}, {x: 8, y: 10}];
        let food = {x: 5, y: 5};
        let dx = 1; let dy = 0;
        let score = 0;
        let gameInterval;
        let gameOver = false;
        let quizActive = false;
        let globalHueShift = 0;
        let pendingWrap = {x: 0, y: 0}; // Remembers where to put the snake after a correct answer

        function startGame() {
            gameOver = false;
            quizActive = false;
            vocabModal.style.display = "none";
            restartBtn.style.display = "none";
            gameInterval = setInterval(update, 105);
        }

        function update() {
            if (quizActive || gameOver) return;
            
            moveSnake();
            if (checkSelfCollision()) { endGame("WASTED (BIT YOURSELF)"); return; }
            checkFoodConsumption();
            globalHueShift = (globalHueShift + 3) % 360;
            draw();
        }

        function moveSnake() {
            let nextX = snake[0].x + dx;
            let nextY = snake[0].y + dy;

            // --- CHECK IF HIT WALL ---
            if (nextX < 0 || nextX >= tileCount || nextY < 0 || nextY >= tileCount) {
                // Wrap Target Destination Mapping Coordinates
                let wrapX = nextX;
                let wrapY = nextY;
                if (nextX < 0) wrapX = tileCount - 1;
                if (nextX >= tileCount) wrapX = 0;
                if (nextY < 0) wrapY = tileCount - 1;
                if (nextY >= tileCount) wrapY = 0;

                // Save destination and pause engine to activate quiz UI
                pendingWrap = { x: wrapX, y: wrapY };
                triggerVocabQuiz();
                return;
            }

            const head = {x: nextX, y: nextY};
            snake.unshift(head);
            snake.pop();
        }

        function triggerVocabQuiz() {
            quizActive = true;
            clearInterval(gameInterval); // Freeze snake movement
            
            // Choose random item from vocab set
            let randomQuiz = VOCAB_BANK[Math.floor(Math.random() * VOCAB_BANK.length)];
            quizQuestion.innerText = randomQuiz.q;
            quizOptions.innerHTML = ""; // Reset old buttons
            
            // Generate shuffling options layout answers dynamically
            randomQuiz.o.forEach(option => {
                let btn = document.createElement("button");
                btn.className = "option-btn";
                btn.innerText = option;
                btn.onclick = () => verifyAnswer(option, randomQuiz.a);
                quizOptions.appendChild(btn);
            });
            
            vocabModal.style.display = "flex"; // Show Quiz Window
        }

        function verifyAnswer(chosen, correct) {
            vocabModal.style.display = "none";
            quizActive = false;
            
            if (chosen === correct) {
                // SUCCESS: Perform saved coordinate warp operation
                const head = { x: pendingWrap.x, y: pendingWrap.y };
                snake.unshift(head);
                snake.pop();
                
                // Resume game loop
                gameInterval = setInterval(update, 105);
            } else {
                // FAILURE: Incorrect vocabulary mapping kills run sequence
                endGame("WRONG ANSWER! GATE LOCKED");
            }
        }

        function checkSelfCollision() {
            const head = snake[0];
            for (let i = 1; i < snake.length; i++) {
                if (snake[i].x === head.x && snake[i].y === head.y) return true;
            }
            return false;
        }

        function checkFoodConsumption() {
            const head = snake[0];
            if (head.x === food.x && head.y === food.y) {
                score += 10;
                scoreElement.innerText = String(score).padStart(3, '0');
                snake.push({ ...snake[snake.length - 1] });
                lengthElement.innerText = snake.length;
                generateFood();
            }
        }

        function generateFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);
        }

        function draw() {
            ctx.fillStyle = "#030307";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Food Core
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(food.x * gridSize + 4, food.y * gridSize + 4, gridSize - 8, gridSize - 8);

            // Snake Rendering Pass Loops
            snake.forEach((cell, index) => {
                let segmentHue = (globalHueShift + (index * 12)) % 360;
                ctx.fillStyle = `hsl(${segmentHue}, 100%, 60%)`;
                ctx.shadowBlur = 6;
                ctx.shadowColor = `hsl(${segmentHue}, 100%, 50%)`;
                ctx.fillRect(cell.x * gridSize + 1, cell.y * gridSize + 1, gridSize - 2, gridSize - 2);
            });
            ctx.shadowBlur = 0;
        }

        function endGame(reasonText) {
            clearInterval(gameInterval);
            gameOver = true;
            ctx.fillStyle = "rgba(0,0,0,0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#ff3366";
            ctx.font = "bold 24px 'Share Tech Mono'";
            ctx.textAlign = "center";
            ctx.fillText(reasonText, canvas.width / 2, canvas.height / 2);
            restartBtn.style.display = "block";
        }

        function resetGame() {
            snake = [{x: 10, y: 10}, {x: 9, y: 10}, {x: 8, y: 10}];
            dx = 1; dy = 0; score = 0;
            scoreElement.innerText = "000";
            lengthElement.innerText = "3";
            generateFood();
            startGame();
        }

        function changeDirection(dir) {
            if (gameOver || quizActive) return;
            if (dir === "UP" && dy !== 1)    { dx = 0; dy = -1; }
            if (dir === "DOWN" && dy !== -1) { dx = 0; dy = 1; }
            if (dir === "LEFT" && dx !== 1)  { dx = -1; dy = 0; }
            if (dir === "RIGHT" && dx !== -1) { dx = 1; dy = 0; }
        }

        window.addEventListener("keydown", e => {
            if(["Space", " ", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();
            if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") changeDirection("UP");
            if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") changeDirection("DOWN");
            if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") changeDirection("LEFT");
            if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") changeDirection("RIGHT");
        });

        document.getElementById("padUp").addEventListener("pointerdown", () => changeDirection("UP"));
        document.getElementById("padDown").addEventListener("pointerdown", () => changeDirection("DOWN"));
        document.getElementById("padLeft").addEventListener("pointerdown", () => changeDirection("LEFT"));
        document.getElementById("padRight").addEventListener("pointerdown", () => changeDirection("RIGHT"));

        startGame();
    </script>
</body>
</html>
"""

# Render Layout Structure
st.markdown('<div class="mobile-container">', unsafe_allow_html=True)
components.html(vocab_snake_html, height=560)
st.markdown('</div>', unsafe_allow_html=True)

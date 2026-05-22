
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="7000-Word Master Snake", page_icon="🐍", layout="centered")

# --- UPGRADED HIGH-VISIBILITY HEADER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: #080711;
    }
    
    /* Neon Sign Header Container */
    .header-box {
        background: linear-gradient(135deg, #13112c 0%, #0a0916 100%);
        border: 3px solid #00ffff;
        border-radius: 16px;
        padding: 20px 10px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2), inset 0 0 15px rgba(0, 255, 255, 0.1);
    }
    
    .arcade-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 2.6rem;
        margin: 0;
        color: #fff;
        letter-spacing: 2px;
        /* Intense double neon shadow glow */
        text-shadow: 0 0 8px #00ffff, 0 0 20px #00ffff, 0 0 30px #0088ff;
    }
    
    .arcade-sub {
        font-family: 'Share Tech Mono', monospace;
        color: #00ffaa;
        margin-top: 8px;
        margin-bottom: 0px;
        font-size: 1rem;
        font-weight: bold;
        letter-spacing: 1px;
        text-shadow: 0 0 5px rgba(0, 255, 170, 0.5);
    }
    
    .mobile-container {
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    </style>
    
    <div class="header-box">
        <h1 class='arcade-title'>SNAKE</h1>
        <p class='arcade-sub'>🎮 7000-WORD VOCABULARY EDITION 🎮</p>
    </div>
""", unsafe_allow_html=True)

# --- GAME ENGINE WITH BUILT-IN CORE ---
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
            border: 2px solid #00ffff;
        }
        #gameCanvas {
            background-color: #030307;
            display: block;
            width: 320px;
            height: 320px;
        }
        
        #vocabModal {
            display: none;
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
            color: #00ffff;
            font-size: 13px;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        .quiz-question {
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 15px;
            min-height: 55px;
            font-family: sans-serif;
            line-height: 1.4;
        }
        .quiz-options {
            display: grid;
            grid-template-columns: 1fr;
            gap: 6px;
            width: 100%;
        }
        .option-btn {
            background: #1c1a30;
            border: 1px solid #00ffff;
            color: #fff;
            padding: 7px;
            border-radius: 6px;
            font-size: 13px;
            cursor: pointer;
            font-family: sans-serif;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .option-btn:active {
            background: #00ffff;
            color: #000;
        }

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
            color: #00ffff;
            border: 2px solid #00ffff;
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
            background: #00ffff;
            color: #000;
        }
        .empty { pointer-events: none; visibility: hidden; }

        .btn-restart {
            margin-top: 10px;
            padding: 8px 20px;
            background: #fff;
            color: #000;
            border: none;
            font-family: sans-serif;
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
        <div>SNAKE: <span id="length" style="color: #00ffff;">3</span></div>
    </div>

    <div class="screen-wrapper">
        <canvas id="gameCanvas" width="400" height="400"></canvas>
        
        <div id="vocabModal">
            <div class="quiz-title">⚠️ WALL HIT! ANSWER TO PASS:</div>
            <div class="quiz-question" id="quizQuestion">Loading...</div>
            <div class="quiz-options" id="quizOptions"></div>
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
        const VOCAB_BANK = [
            { q: "Which word means 'existing or happening at the same time'?", a: "simultaneous", o: ["simultaneous", "spontaneous", "continuous", "obsolete"] },
            { q: "The heavy rain caused ________ damage to the crops in the valley.", a: "considerable", o: ["considerable", "superficial", "artificial", "obvious"] },
            { q: "Which word is a synonym for 'extremely careful about small details'?", a: "meticulous", o: ["meticulous", "arrogant", "indifferent", "ignorant"] },
            { q: "The choice to study abroad was a major ________ in her life.", a: "turning point", o: ["turning point", "compromise", "catastrophe", "coincidence"] },
            { q: "What is the meaning of the word 'abundant'?", a: "plentiful", o: ["plentiful", "rare", "hazardous", "obsolete"] },
            { q: "Due to the lack of evidence, the police had to ________ the suspect.", a: "release", o: ["release", "arrest", "scrutinize", "accumulate"] },
            { q: "Which of the following words means 'impossible to avoid'?", a: "inevitable", o: ["inevitable", "flexible", "improbable", "sustainable"] },
            { q: "Medical simulation helps students learn without ________ patient safety.", a: "compromising", o: ["compromising", "accelerating", "accumulating", "prospering"] },
            { q: "To 'evaluate' something means to ________.", a: "judge its value", o: ["judge its value", "ignore its flaws", "destroy completely", "copy exactly"] },
            { q: "The government took strict measures to ________ the spread of the virus.", a: "contain", o: ["contain", "cherish", "cultivate", "contradict"] },
            { q: "Which word means 'to change or adjust to suit new conditions'?", a: "adapt", o: ["adapt", "adopt", "adore", "adequate"] },
            { q: "The internet has become an ________ part of our daily lives.", a: "indispensable", o: ["indispensable", "indifferent", "innocent", "insignificant"] },
            { q: "She has a ________ memory and can recall events from years ago.", a: "vivid", o: ["vivid", "vague", "vacant", "vulnerable"] },
            { q: "What is a synonym for 'prosper'?", a: "thrive", o: ["thrive", "perish", "precede", "postpone"] },
            { q: "The manager praised Leo for his ________ performance in sales.", a: "outstanding", o: ["outstanding", "outdated", "outrageous", "outward"] },
            { q: "Which word describes something that lasts for only a very short time?", a: "ephemeral", o: ["ephemeral", "eternal", "essential", "eccentric"] },
            { q: "We must find a ________ solution to protect our environment.", a: "sustainable", o: ["sustainable", "vulnerable", "temporary", "superficial"] },
            { q: "The sudden loud noise ________ the sleeping baby.", a: "startled", o: ["startled", "soothed", "satisfied", "stimulated"] },
            { q: "Which word means 'to notice or become aware of something'?", a: "perceive", o: ["perceive", "perish", "persuade", "securing"] },
            { q: "The historical museum contains many rare and precious ________.", a: "artifacts", o: ["artifacts", "artificials", "appliances", "architects"] },
            { q: "She is ________ to peanuts, so she has to check food labels carefully.", a: "allergic", o: ["allergic", "alert", "allowed", "alien"] },
            { q: "What does the word 'reputable' mean?", a: "highly respected", o: ["highly respected", "very repetitive", "untrustworthy", "expensive"] },
            { q: "The two countries signed a treaty to ________ economic cooperation.", a: "enhance", o: ["enhance", "endanger", "enforce", "encounter"] },
            { q: "Which word is the opposite of 'pessimistic'?", a: "optimistic", o: ["optimistic", "indifferent", "aggressive", "depressed"] },
            { q: "The CEO decided to ________ all his energy into the new tech project.", a: "channel", o: ["channel", "challenge", "cherish", "chronicle"] }
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
        let pendingWrap = {x: 0, y: 0};

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
            if (checkSelfCollision()) { endGame("Game Over! Bit your own tail."); return; }
            checkFoodConsumption();
            globalHueShift = (globalHueShift + 3) % 360;
            draw();
        }

        function moveSnake() {
            let nextX = snake[0].x + dx;
            let nextY = snake[0].y + dy;

            if (nextX < 0 || nextX >= tileCount || nextY < 0 || nextY >= tileCount) {
                let wrapX = nextX;
                let wrapY = nextY;
                if (nextX < 0) wrapX = tileCount - 1;
                if (nextX >= tileCount) wrapX = 0;
                if (nextY < 0) wrapY = tileCount - 1;
                if (nextY >= tileCount) wrapY = 0;

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
            clearInterval(gameInterval);
            
            let randomQuiz = VOCAB_BANK[Math.floor(Math.random() * VOCAB_BANK.length)];
            quizQuestion.innerText = randomQuiz.q;
            quizOptions.innerHTML = "";
            
            randomQuiz.o.forEach(option => {
                let btn = document.createElement("button");
                btn.className = "option-btn";
                btn.innerText = option;
                btn.onclick = () => verifyAnswer(option, randomQuiz.a);
                quizOptions.appendChild(btn);
            });
            
            vocabModal.style.display = "flex";
        }

        function verifyAnswer(chosen, correct) {
            vocabModal.style.display = "none";
            quizActive = false;
            
            if (chosen === correct) {
                const head = { x: pendingWrap.x, y: pendingWrap.y };
                snake.unshift(head);
                snake.pop();
                gameInterval = setInterval(update, 105);
            } else {
                endGame("ACCESS DENIED! Wrong Answer.");
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

            ctx.fillStyle = "#ffffff";
            ctx.fillRect(food.x * gridSize + 4, food.y * gridSize + 4, gridSize - 8, gridSize - 8);

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
            ctx.font = "bold 20px sans-serif";
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

st.markdown('<div class="mobile-container">', unsafe_allow_html=True)
components.html(vocab_snake_html, height=560)
st.markdown('</div>', unsafe_allow_html=True)

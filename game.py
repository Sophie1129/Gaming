import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Easy Mobile Snake", page_icon="📱", layout="centered")

# --- LAYOUT STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    .stApp {
        background: #090a15;
    }
    .arcade-title {
        font-family: sans-serif;
        font-weight: 900;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 0px;
        color: #fff;
        text-shadow: 0 0 10px #00ffff;
    }
    .arcade-sub {
        font-family: 'Share Tech Mono', monospace;
        color: #00ff66;
        text-align: center;
        margin-bottom: 15px;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    .mobile-container {
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    </style>
    
    <h1 class='arcade-title'>EASY SNAKE</h1>
    <p class='arcade-sub'>WALL-WRAP ACTIVE // NO WALL CRASHES!</p>
""", unsafe_allow_html=True)

# --- GAME ENGINE WITH WALL-WRAPPING LOOP ---
easy_snake_html = """
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
            border: 2px solid #00ff66; /* Green border to signal it's safe! */
        }
        #gameCanvas {
            background-color: #030307;
            display: block;
            width: 320px;
            height: 320px;
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
            color: #00ff66;
            border: 2px solid #00ff66;
            border-radius: 12px;
            font-size: 22px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 10px rgba(0, 255, 102, 0.1);
            cursor: pointer;
            -webkit-touch-callout: none; 
        }
        .dpad-btn:active {
            background: #00ff66;
            color: #000;
            box-shadow: 0 0 15px #00ff66;
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
            z-index: 10;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
</head>
<body>

    <div class="hud">
        <div>SCORE: <span id="score">000</span></div>
        <div>LENGTH: <span id="length" style="color: #00ff66;">3</span></div>
    </div>

    <div class="screen-wrapper">
        <canvas id="gameCanvas" width="400" height="400"></canvas>
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
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");
        const lengthElement = document.getElementById("length");
        const restartBtn = document.getElementById("restartBtn");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        let snake = [{x: 10, y: 10}, {x: 9, y: 10}, {x: 8, y: 10}];
        let food = {x: 5, y: 5};
        let dx = 1; let dy = 0;
        let score = 0;
        let gameInterval;
        let gameOver = false;
        let globalHueShift = 0;

        function startGame() {
            gameOver = false;
            restartBtn.style.display = "none";
            gameInterval = setInterval(update, 100);
        }

        function update() {
            moveSnake();
            if (checkSelfCollision()) { endGame(); return; }
            checkFoodConsumption();
            globalHueShift = (globalHueShift + 3) % 360;
            draw();
        }

        function moveSnake() {
            let nextX = snake[0].x + dx;
            let nextY = snake[0].y + dy;

            // --- THE EASY WALL-WRAP LOGIC ---
            // If snake goes off the edges, wrap its coordinates to the opposite side
            if (nextX < 0) nextX = tileCount - 1;
            if (nextX >= tileCount) nextX = 0;
            if (nextY < 0) nextY = tileCount - 1;
            if (nextY >= tileCount) nextY = 0;

            const head = {x: nextX, y: nextY};
            snake.unshift(head);
            snake.pop();
        }

        function checkSelfCollision() {
            const head = snake[0];
            // Game over only happens if you crash into your OWN body tail segments now!
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

            // Rainbow snake tail blocks
            snake.forEach((cell, index) => {
                let segmentHue = (globalHueShift + (index * 12)) % 360;
                ctx.fillStyle = `hsl(${segmentHue}, 100%, 60%)`;
                ctx.shadowBlur = 6;
                ctx.shadowColor = `hsl(${segmentHue}, 100%, 50%)`;
                ctx.fillRect(cell.x * gridSize + 1, cell.y * gridSize + 1, gridSize - 2, gridSize - 2);
            });
            ctx.shadowBlur = 0;
        }

        function endGame() {
            clearInterval(gameInterval);
            gameOver = true;
            ctx.fillStyle = "rgba(0,0,0,0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#ff3366";
            ctx.font = "bold 28px 'Share Tech Mono'";
            ctx.textAlign = "center";
            ctx.fillText("WASTED (BIT YOURSELF)", canvas.width / 2, canvas.height / 2);
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
            if (gameOver) return;
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

# Render Frame layout
st.markdown('<div class="mobile-container">', unsafe_allow_html=True)
components.html(easy_snake_html, height=560)
st.markdown('</div>', unsafe_allow_html=True)

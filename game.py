import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mobile Prism Snake", page_icon="📱", layout="centered")

# --- MOBILE LAYOUT TUNING ---
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
        color: #666;
        text-align: center;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }
    /* Centers our game frame nicely on mobile viewports */
    .mobile-container {
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    </style>
    
    <h1 class='arcade-title'>TOUCH SNAKE</h1>
    <p class='arcade-sub'>TAP ARROWS BELOW OR SWIPE TO STEER</p>
""", unsafe_allow_html=True)

# --- GAME ENGINE WITH TOUCH CONTROLS ---
mobile_snake_html = """
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
            user-select: none; /* Prevents text selection highlighting on accidental double taps */
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
            border: 2px solid #333;
        }
        #gameCanvas {
            background-color: #030307;
            display: block;
            width: 320px;   /* Fixed crisp size scaled down dynamically for mobile viewports */
            height: 320px;
        }
        
        /* VIRTUAL TOUCH D-PAD LAYOUT */
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
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.1);
            cursor: pointer;
            /* Prevents long-press context menus pops up on mobile Chrome/Safari */
            -webkit-touch-callout: none; 
        }
        .dpad-btn:active {
            background: #00ffff;
            color: #000;
            box-shadow: 0 0 15px #00ffff;
        }
        /* Keep grid slots blank to arrange layout natively into a cross D-pad shape */
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
        <div>LENGTH: <span id="length" style="color: #00ffff;">3</span></div>
    </div>

    <div class="screen-wrapper">
        <canvas id="gameCanvas" width="400" height="400"></canvas>
    </div>
    
    <button id="restartBtn" class="btn-restart" onclick="resetGame()">TAP TO RESTART</button>

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
            gameInterval = setInterval(update, 110); // Slightly slower grid cycle to make touch maneuvering manageable
        }

        function update() {
            moveSnake();
            if (checkCollision()) { endGame(); return; }
            checkFoodConsumption();
            globalHueShift = (globalHueShift + 3) % 360;
            draw();
        }

        function moveSnake() {
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};
            snake.unshift(head);
            snake.pop();
        }

        function checkCollision() {
            const head = snake[0];
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) return true;
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

            // Target Food Element
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(food.x * gridSize + 4, food.y * gridSize + 4, gridSize - 8, gridSize - 8);

            // Rendering Chameleon Skin
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
            ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2);
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

        // CONTROL LOGIC INTERFACE BINDING (Separated to safely map touch and keyboard events simultaneously)
        function changeDirection(dir) {
            if (gameOver) return;
            if (dir === "UP" && dy !== 1)    { dx = 0; dy = -1; }
            if (dir === "DOWN" && dy !== -1) { dx = 0; dy = 1; }
            if (dir === "LEFT" && dx !== 1)  { dx = -1; dy = 0; }
            if (dir === "RIGHT" && dx !== -1) { dx = 1; dy = 0; }
        }

        // Physical Keyboard Fallback Listeners
        window.addEventListener("keydown", e => {
            if(["Space", " ", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();
            if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") changeDirection("UP");
            if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") changeDirection("DOWN");
            if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") changeDirection("LEFT");
            if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") changeDirection("RIGHT");
        });

        // Virtual On-Screen Button Mapping (Uses pointerdown to instantly track clicks/taps without 300ms mobile delay)
        document.getElementById("padUp").addEventListener("pointerdown", () => changeDirection("UP"));
        document.getElementById("padDown").addEventListener("pointerdown", () => changeDirection("DOWN"));
        document.getElementById("padLeft").addEventListener("pointerdown", () => changeDirection("LEFT"));
        document.getElementById("padRight").addEventListener("pointerdown", () => changeDirection("RIGHT"));

        startGame();
    </script>
</body>
</html>
"""

# Render framework adjusting frame size for both Canvas element + Control Grid array height
st.markdown('<div class="mobile-container">', unsafe_allow_html=True)
components.html(mobile_snake_html, height=560)
st.markdown('</div>', unsafe_allow_html=True)

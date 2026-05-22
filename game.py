import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chameleon Snake", page_icon="🌈", layout="centered")

# --- CABINET FRAME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Viper+Bite&display=swap');
    
    .stApp {
        background: radial-gradient(circle, #090a15 0%, #020205 100%);
    }
    .arcade-title {
        font-family: sans-serif;
        font-weight: 900;
        letter-spacing: 4px;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0px;
        color: #fff;
        text-shadow: 0 0 10px #ff007f, 0 0 20px #00ffff;
    }
    .arcade-sub {
        font-family: 'Share Tech Mono', monospace;
        color: #888;
        text-align: center;
        margin-bottom: 25px;
        font-size: 1rem;
    }
    .cabinet-frame {
        background: #05050a;
        border: 4px dashed #333;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.05);
        max-width: 460px;
        margin: 0 auto;
    }
    </style>
    
    <h1 class='arcade-title'>PRISM SNAKE</h1>
    <p class='arcade-sub'>WATCH THE SKIN SHIFT COLOR AS YOU EXTEND</p>
""", unsafe_allow_html=True)

# --- GAME ENGINE WITH RAINBOW JAVASCRIPT MODIFICATION ---
rainbow_snake_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            overflow: hidden;
            font-family: 'Share Tech Mono', monospace;
        }
        .screen-wrapper {
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            border: 3px solid #333;
        }
        #gameCanvas {
            background-color: #030307;
            display: block;
        }
        .hud {
            width: 400px;
            display: flex;
            justify-content: space-between;
            color: #fff;
            font-size: 22px;
            margin-bottom: 12px;
        }
        .btn-neon {
            margin-top: 15px;
            padding: 10px 25px;
            background: #fff;
            color: #000;
            border: none;
            font-family: 'Share Tech Mono', monospace;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            display: none;
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
    
    <button id="restartBtn" class="btn-neon" onclick="resetGame()">RESTART</button>

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
        
        // This variable ticks up every frame to shift the color spectrum globally
        let globalHueShift = 0; 

        function startGame() {
            gameOver = false;
            restartBtn.style.display = "none";
            gameInterval = setInterval(update, 90);
        }

        function update() {
            moveSnake();
            if (checkCollision()) { endGame(); return; }
            checkFoodConsumption();
            
            // Advance the color wheel cycle slightly every frame
            globalHueShift = (globalHueShift + 2) % 360; 
            
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

            // Draw Food (White Core)
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(food.x * gridSize + 4, food.y * gridSize + 4, gridSize - 8, gridSize - 8);

            // DRAW THE COLOR-CHANGING SNAKE
            snake.forEach((cell, index) => {
                // Formula combines the frame time (globalHueShift) and body segment index
                // This creates an animated "wave" of rainbow colors flowing down the body
                let segmentHue = (globalHueShift + (index * 12)) % 360;
                
                // Use HSL color space: Hue (0-360), Saturation (100%), Lightness (60%)
                ctx.fillStyle = `hsl(${segmentHue}, 100%, 60%)`;
                
                // Apply a glowing neon shadow matching the segment's current color
                ctx.shadowBlur = 10;
                ctx.shadowColor = `hsl(${segmentHue}, 100%, 50%)`;
                
                let x = cell.x * gridSize + 1;
                let y = cell.y * gridSize + 1;
                let size = gridSize - 2;
                ctx.fillRect(x, y, size, size);
            });
            
            // Turn off shadows so they don't drag down performance elsewhere
            ctx.shadowBlur = 0;
        }

        function endGame() {
            clearInterval(gameInterval);
            gameOver = true;
            ctx.fillStyle = "rgba(0,0,0,0.8)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#fff";
            ctx.font = "bold 30px 'Share Tech Mono'";
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

        window.addEventListener("keydown", e => {
            if (gameOver) return;
            if(["Space", " ", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();
            switch (e.key) {
                case "ArrowUp": case "w": case "W": if (dy !== 1) { dx = 0; dy = -1; } break;
                case "ArrowDown": case "s": case "S": if (dy !== -1) { dx = 0; dy = 1; } break;
                case "ArrowLeft": case "a": case "A": if (dx !== 1) { dx = -1; dy = 0; } break;
                case "ArrowRight": case "d": case "D": if (dx !== -1) { dx = 1; dy = 0; } break;
            }
        });

        startGame();
    </script>
</body>
</html>
"""

# Render framework
st.markdown('<div class="cabinet-frame">', unsafe_allow_html=True)
components.html(rainbow_snake_html, height=520)
st.markdown('</div>', unsafe_allow_html=True)

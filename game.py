import streamlit as st
import streamlit.components.v1 as components

# Set up page config
st.set_page_config(page_title="Neon Snake Arcade", page_icon="🐍", layout="centered")

# --- STREAMLIT UI & CABINET DECORATION ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Share+Tech+Mono&display=swap');
    
    /* Neon Cyberpunk Background */
    .stApp {
        background: radial-gradient(circle, #1a0b2e 0%, #05020a 100%);
    }
    
    /* Reto Arcade Logo Styling */
    .arcade-title {
        font-family: 'Permanent Marker', cursive;
        color: #fff;
        text-align: center;
        font-size: 3.5rem;
        margin-bottom: 0px;
        background: linear-gradient(to right, #ff007f, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(255,0,127,0.6));
    }
    
    .arcade-sub {
        font-family: 'Share Tech Mono', monospace;
        color: #00ffff;
        text-align: center;
        margin-bottom: 25px;
        font-size: 1.1rem;
        letter-spacing: 2px;
        text-shadow: 0 0 8px #00ffff;
    }

    /* Outer Arcade Cabinet Wrapper Box */
    .cabinet-frame {
        background: #0d021a;
        border: 4px solid #ff007f;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 35px rgba(255, 0, 127, 0.4), inset 0 0 20px rgba(0, 255, 255, 0.2);
        max-width: 460px;
        margin: 0 auto;
    }
    </style>
    
    <h1 class='arcade-title'>CYBER SNAKE</h1>
    <p class='arcade-sub'>INSERT COIN // USE ARROWS OR WASD</p>
""", unsafe_allow_html=True)

# --- EMBEDDED JAVASCRIPT ENGINE WITH DECORATIONS ---
decorated_snake_html = """
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
        
        /* CRT Monitor Screen Frame and Glow */
        .screen-wrapper {
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            border: 3px solid #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        }

        /* Animated Scanline Overlay Effect for Vintage CRT look */
        .screen-wrapper::after {
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 2;
            background-size: 100% 4px, 6px 100%;
            pointer-events: none;
        }

        #gameCanvas {
            background-color: #08020f;
            display: block;
        }

        /* Top HUD Dashboard */
        .hud {
            width: 400px;
            display: flex;
            justify-content: space-between;
            color: #00ffff;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 1px;
            margin-bottom: 12px;
            text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
        }

        /* Premium Cyberpunk Restart Button */
        .btn-neon {
            margin-top: 15px;
            padding: 10px 25px;
            background: transparent;
            color: #ff007f;
            border: 2px solid #ff007f;
            font-family: 'Share Tech Mono', monospace;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 2px;
            cursor: pointer;
            border-radius: 4px;
            text-shadow: 0 0 8px #ff007f;
            box-shadow: 0 0 10px rgba(255,0,127,0.2), inset 0 0 10px rgba(255,0,127,0.2);
            transition: all 0.2s ease;
            display: none;
        }
        .btn-neon:hover {
            color: #fff;
            background: #ff007f;
            box-shadow: 0 0 20px #ff007f;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
</head>
<body>

    <div class="hud">
        <div>SCORE: <span id="score" style="color: #fff;">000</span></div>
        <div style="color: #ff007f;">HI-SCORE: <span id="hiscore" style="color: #fff;">000</span></div>
    </div>

    <div class="screen-wrapper">
        <canvas id="gameCanvas" width="400" height="400"></canvas>
    </div>
    
    <button id="restartBtn" class="btn-neon" onclick="resetGame()">SYSTEM REBOOT</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");
        const hiscoreElement = document.getElementById("hiscore");
        const restartBtn = document.getElementById("restartBtn");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        let snake = [{x: 10, y: 10}, {x: 9, y: 10}, {x: 8, y: 10}];
        let food = {x: 5, y: 5};
        let dx = 1;
        let dy = 0;
        let score = 0;
        let hiscore = 0;
        let gameInterval;
        let gameOver = false;

        function startGame() {
            gameOver = false;
            restartBtn.style.display = "none";
            gameInterval = setInterval(update, 90); // Slightly faster for slicker gameplay
        }

        function update() {
            moveSnake();
            if (checkCollision()) { endGame(); return; }
            checkFoodConsumption();
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
                if (score > hiscore) {
                    hiscore = score;
                    hiscoreElement.innerText = String(hiscore).padStart(3, '0');
                }
                snake.push({ ...snake[snake.length - 1] });
                generateFood();
            }
        }

        function generateFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);
            for(let cell of snake) {
                if(cell.x === food.x && cell.y === food.y) { generateFood(); break; }
            }
        }

        function draw() {
            // Draw background grid lines faintly
            ctx.fillStyle = "#0c0418";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.strokeStyle = "rgba(0, 255, 255, 0.03)";
            ctx.lineWidth = 1;
            for(let i=0; i<canvas.width; i+=gridSize) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(canvas.width, i); ctx.stroke();
            }

            // Setup glowing effects for standard draws
            ctx.shadowBlur = 12;

            // Draw Food (Glowing Neon Red Core)
            ctx.shadowColor = "#ff007f";
            ctx.fillStyle = "#ff007f";
            ctx.fillRect(food.x * gridSize + 2, food.y * gridSize + 2, gridSize - 4, gridSize - 4);
            // Highlight inner circle
            ctx.fillStyle = "#fff";
            ctx.fillRect(food.x * gridSize + 6, food.y * gridSize + 6, gridSize - 12, gridSize - 12);

            // Draw Snake with Gradient Colors & Cyan Glow
            ctx.shadowColor = "#00ffff";
            snake.forEach((cell, index) => {
                // Creates a fade effect down the tail from Cyan to Purple
                let hue = 180 + (index * 5); 
                ctx.fillStyle = `hsl(${hue}, 100%, 60%)`;
                
                // Rounded corner box looks better than hard edges
                let x = cell.x * gridSize + 1;
                let y = cell.y * gridSize + 1;
                let size = gridSize - 2;
                ctx.fillRect(x, y, size, size);
            });
            
            // Turn off shadows for text elements
            ctx.shadowBlur = 0;
        }

        function endGame() {
            clearInterval(gameInterval);
            gameOver = true;
            
            ctx.fillStyle = "rgba(8, 2, 15, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Neon Error Text
            ctx.fillStyle = "#ff007f";
            ctx.font = "bold 32px 'Share Tech Mono'";
            ctx.textAlign = "center";
            ctx.fillText("CRITICAL FAILURE", canvas.width / 2, canvas.height / 2 - 10);
            
            ctx.fillStyle = "#00ffff";
            ctx.font = "20px 'Share Tech Mono'";
            ctx.fillText("SCORE DETECTED: " + score, canvas.width / 2, canvas.height / 2 + 25);
            
            restartBtn.style.display = "block";
        }

        function resetGame() {
            snake = [{x: 10, y: 10}, {x: 9, y: 10}, {x: 8, y: 10}];
            dx = 1; dy = 0; score = 0;
            scoreElement.innerText = "000";
            generateFood();
            startGame();
        }

        // Catch commands safely
        window.addEventListener("keydown", e => {
            if (gameOver) return;
            if(["Space", " ", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
                e.preventDefault();
            }
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

# Render inside the decorated HTML macro frame setup
st.markdown('<div class="cabinet-frame">', unsafe_allow_html=True)
components.html(decorated_snake_html, height=520)
st.markdown('</div>', unsafe_allow_html=True)

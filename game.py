import streamlit as st
import streamlit.components.v1 as components

# Set up page config
st.set_page_config(page_title="Streamlit Snake Arcade", page_icon="🐍", layout="centered")

# --- STREAMLIT UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=css');
    
    .arcade-title {
        font-family: 'Press Start 2P', monospace;
        color: #39FF14;
        text-align: center;
        text-shadow: 0 0 10px #39FF14;
        margin-bottom: 5px;
        font-size: 2rem;
    }
    .arcade-sub {
        font-family: sans-serif;
        color: #888;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    <h1 class='arcade-title'>SNAKE.EXE</h1>
    <p class='arcade-sub'>Use your keyboard <b>Arrow Keys</b> or <b>WASD</b> to steer. Avoid the walls and your own tail!</p>
""", unsafe_allow_html=True)

# --- EMBEDDED HTML5 / JAVASCRIPT GAME ENGINE ---
snake_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #0e1117;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            font-family: 'Courier New', Courier, monospace;
        }
        #gameCanvas {
            border: 4px solid #333;
            background-color: #111;
            box-shadow: 0 0 20px rgba(57, 255, 20, 0.2);
        }
        #scoreBoard {
            color: #fff;
            font-size: 24px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .btn-restart {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #39FF14;
            color: black;
            border: none;
            font-weight: bold;
            cursor: pointer;
            border-radius: 5px;
            display: none; /* Shown only on Game Over */
        }
    </style>
</head>
<body>

    <div id="scoreBoard">SCORE: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <button id="restartBtn" class="btn-restart" onclick="resetGame()">PLAY AGAIN</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");
        const restartBtn = document.getElementById("restartBtn");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;

        let snake = [{x: 10, y: 10}];
        let food = {x: 5, y: 5};
        let dx = 1;
        let dy = 0;
        let score = 0;
        let gameInterval;
        let gameOver = false;

        // Main game loop manager
        function startGame() {
            gameOver = false;
            restartBtn.style.display = "none";
            gameInterval = setInterval(update, 100); // 100ms per frame (Smooth arcade speed)
        }

        // Handle game updates per frame
        function update() {
            moveSnake();
            
            if (checkCollision()) {
                endGame();
                return;
            }

            checkFoodConsumption();
            draw();
        }

        // Move head position and shift body array
        function moveSnake() {
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};
            snake.unshift(head);
            snake.pop(); // Remove tail unless eating food
        }

        // Check if head hits wall or itself
        function checkCollision() {
            const head = snake[0];
            
            // Wall collisions
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                return true;
            }
            
            // Tail collisions
            for (let i = 1; i < snake.length; i++) {
                if (snake[i].x === head.x && snake[i].y === head.y) {
                    return true;
                }
            }
            return false;
        }

        // Check if head reaches food
        function checkFoodConsumption() {
            const head = snake[0];
            if (head.x === food.x && head.y === food.y) {
                score += 10;
                scoreElement.innerText = score;
                
                // Grow snake by duplicating the tail
                snake.push({ ...snake[snake.length - 1] });
                
                generateFood();
            }
        }

        // Spawn food at a random grid coordinate
        function generateFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);
            
            // Ensure food doesn't spawn inside snake body
            for(let cell of snake) {
                if(cell.x === food.x && cell.y === food.y) {
                    generateFood();
                    break;
                }
            }
        }

        // Render objects on Canvas
        function draw() {
            // Clear canvas
            ctx.fillStyle = "#111";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw Snake
            snake.forEach((cell, index) => {
                ctx.fillStyle = index === 0 ? "#39FF14" : "#22aa0e"; // Bright green head, darker green body
                ctx.fillRect(cell.x * gridSize, cell.y * gridSize, gridSize - 2, gridSize - 2);
            });

            // Draw Food
            ctx.fillStyle = "#FF3131"; // Neon Red Food
            ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
        }

        function endGame() {
            clearInterval(gameInterval);
            gameOver = true;
            
            // Draw Game Over text overlay
            ctx.fillStyle = "rgba(0,0,0,0.75)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#FF3131";
            ctx.font = "30px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);
            
            ctx.fillStyle = "#fff";
            ctx.font = "16px sans-serif";
            ctx.fillText("Final Score: " + score, canvas.width / 2, canvas.height / 2 + 20);
            
            restartBtn.style.display = "block";
        }

        function resetGame() {
            snake = [{x: 10, y: 10}];
            dx = 1;
            dy = 0;
            score = 0;
            scoreElement.innerText = score;
            generateFood();
            startGame();
        }

        // Listen for Keyboard Input (Supports Arrows and WASD)
        window.addEventListener("keydown", e => {
            if (gameOver) return;
            
            switch (e.key) {
                case "ArrowUp":
                case "w":
                case "W":
                    if (dy !== 1) { dx = 0; dy = -1; }
                    break;
                case "ArrowDown":
                case "s":
                case "S":
                    if (dy !== -1) { dx = 0; dy = 1; }
                    break;
                case "ArrowLeft":
                case "a":
                case "A":
                    if (dx !== 1) { dx = -1; dy = 0; }
                    break;
                case "ArrowRight":
                case "d":
                case "D":
                    if (dx !== -1) { dx = 1; dy = 0; }
                    break;
            }
        });

        // Start the engine on page load
        startGame();
    </script>
</body>
</html>
"""

# Render the HTML component inside Streamlit frame
components.html(snake_game_html, height=520)

# --- SIDEBAR INFO ---
with st.sidebar:
    st.header("🕹️ Retro Cabinet Controls")
    st.markdown("""
    This app showcases how to use **HTML5 Canvas** inside Streamlit to bypass server latency constraints.
    
    * **Engine:** Pure JavaScript Canvas
    * **Graphics:** 60 FPS Emulated Loop
    * **Styling:** CSS Neon-Glow theme
    """)

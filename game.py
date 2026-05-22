import streamlit as st
import streamlit.components.v1 as components

# Set up page config
st.set_page_config(page_title="Streamlit Space Arcade", page_icon="🚀", layout="centered")

# --- STREAMLIT UI & CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .arcade-title {
        font-family: 'Orbitron', sans-serif;
        color: #00ffff;
        text-align: center;
        text-shadow: 0 0 15px #00ffff;
        margin-bottom: 5px;
        font-size: 2.5rem;
    }
    .arcade-sub {
        font-family: 'Orbitron', sans-serif;
        color: #ff007f;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1rem;
        text-shadow: 0 0 5px #ff007f;
    }
    .stApp {
        background-color: #05050a;
    }
    </style>
    <h1 class='arcade-title'>SPACE SHOOTER.EXE</h1>
    <p class='arcade-sub'>◄ ► or A/D to Move | SPACEBAR to Shoot</p>
""", unsafe_allow_html=True)

# --- EMBEDDED HTML5 / JAVASCRIPT GAME ENGINE ---
shooting_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #05050a;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            font-family: 'Orbitron', sans-serif;
            overflow: hidden;
        }
        #gameCanvas {
            border: 3px solid #00ffff;
            background-color: #000;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.3);
        }
        .ui-container {
            display: flex;
            justify-content: space-between;
            width: 500px;
            color: #fff;
            font-size: 18px;
            margin-bottom: 10px;
            text-shadow: 0 0 5px #fff;
        }
        #scoreBoard { color: #00ff66; }
        #livesBoard { color: #ff3333; }
        .btn-restart {
            margin-top: 15px;
            padding: 12px 25px;
            background-color: #ff007f;
            color: white;
            border: none;
            font-family: 'Orbitron', sans-serif;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            box-shadow: 0 0 15px #ff007f;
            display: none;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>

    <div class="ui-container">
        <div id="scoreBoard">SCORE: <span id="score">0</span></div>
        <div id="livesBoard">LIVES: <span id="lives">3</span></div>
    </div>
    <canvas id="gameCanvas" width="500" height="500"></canvas>
    <button id="restartBtn" class="btn-restart" onclick="resetGame()">REDEPLOY</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");
        const livesElement = document.getElementById("lives");
        const restartBtn = document.getElementById("restartBtn");

        // Game Variables
        let player = { x: 225, y: 440, width: 40, height: 30, speed: 7 };
        let bullets = [];
        let enemies = [];
        let keys = {};
        let score = 0;
        let lives = 3;
        let gameOver = false;
        let gameLoopId;
        let enemySpawnTimer = 0;

        function startGame() {
            gameOver = false;
            restartBtn.style.display = "none";
            bullets = [];
            enemies = [];
            score = 0;
            lives = 3;
            scoreElement.innerText = score;
            livesElement.innerText = lives;
            gameLoop();
        }

        // Main 60FPS Game Loop
        function gameLoop() {
            if (gameOver) return;

            update();
            draw();

            gameLoopId = requestAnimationFrame(gameLoop);
        }

        function update() {
            // Player Movement
            if (keys["ArrowLeft"] || keys["a"] || keys["A"]) {
                if (player.x > 0) player.x -= player.speed;
            }
            if (keys["ArrowRight"] || keys["d"] || keys["D"]) {
                if (player.x < canvas.width - player.width) player.x += player.speed;
            }

            # Update Bullets
            for (let i = bullets.length - 1; i >= 0; i--) {
                bullets[i].y -= bullets[i].speed;
                if (bullets[i].y < 0) {
                    bullets.splice(i, 1);
                }
            }

            // Spawn Enemies
            enemySpawnTimer++;
            if (enemySpawnTimer > 40) { // Spawns an enemy roughly every 40 frames
                let size = Math.random() * 20 + 20;
                enemies.push({
                    x: Math.random() * (canvas.width - size),
                    y: -size,
                    width: size,
                    height: size,
                    speed: Math.random() * 2 + 1.5
                });
                enemySpawnTimer = 0;
            }

            // Update Enemies
            for (let i = enemies.length - 1; i >= 0; i--) {
                enemies[i].y += enemies[i].speed;

                // Enemy goes past the screen
                if (enemies[i].y > canvas.height) {
                    enemies.splice(i, 1);
                    lives--;
                    livesElement.innerText = lives;
                    if (lives <= 0) endGame();
                    continue;
                }

                // Collision: Enemy hits Player
                if (checkCollision(enemies[i], player)) {
                    enemies.splice(i, 1);
                    lives--;
                    livesElement.innerText = lives;
                    if (lives <= 0) endGame();
                    continue;
                }

                // Collision: Bullet hits Enemy
                for (let j = bullets.length - 1; j >= 0; j--) {
                    if (checkCollision(bullets[j], enemies[i])) {
                        enemies.splice(i, 1);
                        bullets.splice(j, 1);
                        score += 10;
                        scoreElement.innerText = score;
                        break;
                    }
                }
            }
        }

        function checkCollision(rect1, rect2) {
            return rect1.x < rect2.x + rect2.width &&
                   rect1.x + rect1.width > rect2.x &&
                   rect1.y < rect2.y + rect2.height &&
                   rect1.y + rect1.height > rect2.y;
        }

        function draw() {
            // Clear Frame
            ctx.fillStyle = "#000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw Background Stars (Simple matrix effect)
            ctx.fillStyle = "rgba(255, 255, 255, 0.3)";
            for(let i=0; i<10; i++) {
                ctx.fillRect(Math.random()*canvas.width, Math.random()*canvas.height, 2, 2);
            }

            // Draw Player Ship (Neon Triangle Style)
            ctx.strokeStyle = "#00ffff";
            ctx.lineWidth = 3;
            ctx.fillStyle = "#002b2b";
            ctx.beginPath();
            ctx.moveTo(player.x + player.width / 2, player.y);
            ctx.lineTo(player.x, player.y + player.height);
            ctx.lineTo(player.x + player.width, player.y + player.height);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // Draw Bullets (Neon Lasers)
            ctx.fillStyle = "#ff007f";
            bullets.forEach(bullet => {
                ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
            });

            // Draw Enemies (Neon Hexagons/Squares)
            ctx.strokeStyle = "#ffcc00";
            ctx.fillStyle = "#332200";
            ctx.lineWidth = 2;
            enemies.forEach(enemy => {
                ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
                ctx.strokeRect(enemy.x, enemy.y, enemy.width, enemy.height);
            });
        }

        function endGame() {
            gameOver = true;
            cancelAnimationFrame(gameLoopId);

            // Dark overlay
            ctx.fillStyle = "rgba(5, 5, 10, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Game Over Text
            ctx.fillStyle = "#ff3333";
            ctx.font = "bold 36px Orbitron";
            ctx.textAlign = "center";
            ctx.fillText("MISSION FAILED", canvas.width / 2, canvas.height / 2 - 20);

            ctx.fillStyle = "#fff";
            ctx.font = "18px Orbitron";
            ctx.fillText("FINAL SCORE: " + score, canvas.width / 2, canvas.height / 2 + 20);

            restartBtn.style.display = "block";
        }

        function resetGame() {
            startGame();
        }

        // Input Listeners
        window.addEventListener("keydown", e => {
            keys[e.key] = true;
            
            // Prevent space and arrow keys from scrolling the Streamlit page
            if(["Space", " ", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
                e.preventDefault();
            }

            // Fire Bullet on Spacebar press down
            if ((e.key === " " || e.key === "Spacebar") && !gameOver) {
                bullets.push({
                    x: player.x + player.width / 2 - 2,
                    y: player.y,
                    width: 4,
                    height: 15,
                    speed: 8
                });
            }
        });

        window.addEventListener("keyup", e => {
            keys[e.key] = false;
        });

        // Initialize Engine
        startGame();
    </script>
</body>
</html>
"""

# Render the HTML component inside the Streamlit UI
components.html(shooting_game_html, height=580)

# --- SIDEBAR INFO ---
with st.sidebar:
    st.header("🛸 Galaxy Defence Intel")
    st.markdown("""
    By nesting an HTML5 script into Streamlit, keyboard events bypass the server completely, avoiding latency.
    
    * **Engine:** `requestAnimationFrame` (60 FPS)
    * **Rendering:** HTML5 Context 2D
    * **Controls:** * `A` / `D` or Left / Right Arrows to steer.
      * `Spacebar` to fire lasers.
    """)

const socket = io();
const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');
let gridSize = 50;
let tokens = {};
const emojis = ['😀', '😂', '😍', '😎', '😜', '🤔', '😢', '😡', '🤖', '👻'];

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('update_grid_size', (data) => {
    gridSize = data.gridSize;
    drawGrid();
});

socket.on('update_token_position', (data) => {
    tokens[data.tokenName] = { x: data.x, y: data.y };
    drawTokens();
});

function drawGrid() {
    console.log('Drawing grid');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#ddd';
    for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    drawTokens();
}

function drawTokens() {
    console.log('Drawing tokens');
    for (const [name, pos] of Object.entries(tokens)) {
        console.log(`Drawing token: ${name} at (${pos.x}, ${pos.y})`);
        ctx.fillText(name, pos.x, pos.y + gridSize / 2);
    }
}

function createEmojiTokens() {
    const tokenContainer = document.getElementById('token-container');
    emojis.forEach((emoji, index) => {
        const token = document.createElement('div');
        token.className = 'token';
        token.draggable = true;
        token.innerText = emoji;
        token.id = `token-${index}`;
        token.addEventListener('dragstart', handleDragStart);
        tokenContainer.appendChild(token);
    });
}

function handleDragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.id);
}

canvas.addEventListener('dragover', (event) => {
    event.preventDefault();
});

canvas.addEventListener('drop', (event) => {
    event.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const tokenId = event.dataTransfer.getData('text/plain');
    const tokenElement = document.getElementById(tokenId);
    const tokenName = tokenElement.innerText;
    tokens[tokenName] = { x: x, y: y };
    socket.emit('move_token', { tokenName: tokenName, x: x, y: y });
    drawTokens();
});

createEmojiTokens();
drawGrid();

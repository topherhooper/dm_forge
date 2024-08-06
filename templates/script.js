const socket = io();
const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');
let gridSize = 50;
let tokens = {};

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('update_grid_size', (data) => {
    gridSize = data.gridSize;
    drawGrid();
});

socket.on('update_tokens', (data) => {
    tokens[data.tokenName] = { x: data.x, y: data.y };
    drawTokens();
});

socket.on('update_token_position', (data) => {
    tokens[data.tokenName] = { x: data.x, y: data.y };
    drawTokens();
});

function setGridSize() {
    const size = document.getElementById('grid-size').value;
    socket.emit('set_grid_size', { gridSize: parseInt(size) });
}

function addToken() {
    const name = document.getElementById('token-name').value;
    const x = parseInt(document.getElementById('token-x').value);
    const y = parseInt(document.getElementById('token-y').value);
    socket.emit('add_token', { tokenName: name, x: x, y: y });
    console.log(`Token added: ${name} at (${x}, ${y})`);
}

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
        ctx.fillStyle = 'red';
        ctx.fillRect(pos.x, pos.y, gridSize, gridSize);
        ctx.fillStyle = 'black';
        ctx.fillText(name, pos.x, pos.y + gridSize / 2);
    }
}

canvas.addEventListener('click', (event) => {
    console.log('Canvas clicked');
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    console.log(`Click position: (${x}, ${y})`);
    for (const [name, pos] of Object.entries(tokens)) {
        if (x >= pos.x && x <= pos.x + gridSize && y >= pos.y && y <= pos.y + gridSize) {
            const newX = Math.floor(Math.random() * canvas.width);
            const newY = Math.floor(Math.random() * canvas.height);
            console.log(`Moving token: ${name} to (${newX}, ${newY})`);
            socket.emit('move_token', { tokenName: name, x: newX, y: newY });
            break;
        }
    }
});

drawGrid();
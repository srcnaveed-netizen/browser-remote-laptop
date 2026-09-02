const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

// Security: Password Protect the Web Interface
app.use((req, res, next) => {
    const b64auth = (req.headers.authorization || '').split(' ')[1] || '';
    const [login, password] = Buffer.from(b64auth, 'base64').toString().split(':');

    // YOUR LOGIN DETAILS:
    if (login === 'admin' && password === 'school123') {
        return next();
    }

    res.set('WWW-Authenticate', 'Basic realm="Secure Area"');
    res.status(401).send('Authentication required to access this laptop.');
});

// Serve the web interface
app.use(express.static('public'));

let homeLaptopSocket = null;

io.on('connection', (socket) => {
    console.log('New connection:', socket.id);

    // Identify the home laptop
    socket.on('register_host', () => {
        homeLaptopSocket = socket;
        console.log('🏠 Home laptop is online and connected!');
    });

    // Receive video frames from Home Laptop and broadcast to the Web Browser
    socket.on('screen_frame', (frameData) => {
        socket.broadcast.emit('screen_frame', frameData);
    });

    // Receive controls from Web Browser and send to Home Laptop
    socket.on('mouse_move', (data) => {
        if (homeLaptopSocket) homeLaptopSocket.emit('mouse_move', data);
    });
    socket.on('mouse_click', (data) => {
        if (homeLaptopSocket) homeLaptopSocket.emit('mouse_click', data);
    });
    socket.on('key_press', (data) => {
        if (homeLaptopSocket) homeLaptopSocket.emit('key_press', data);
    });

    socket.on('disconnect', () => {
        if (homeLaptopSocket === socket) {
            homeLaptopSocket = null;
            console.log('🏠 Home laptop disconnected.');
        }
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));

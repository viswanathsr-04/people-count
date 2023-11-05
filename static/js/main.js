// const canvas = document.getElementById('canvas');
// const context = canvas.getContext('2d');

// navigator.mediaDevices.getUserMedia({ video: true })
//     .then((stream) => {
//         video.srcObject = stream;
//         video.play();
//     });

// setInterval(() => {
//     fetch('/detect')
//         .then((response) => response.json())
//         .then((data) => {
//             const count = data.count;
//             const message = `Number of people: ${count}`;
//             document.getElementById('message').textContent = message;
//         });
// }, 1000);
const video = document.getElementById('video');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
let isStreaming = false;

function startStreaming() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            video.play();
            isStreaming = true;
        })
        .catch((err) => {
            console.log('An error occurred: ' + err);
        });
}

function stopStreaming() {
    if (video.srcObject) {
        video.srcObject.getTracks().forEach((track) => {
            track.stop();
        });
        video.srcObject = null;
        isStreaming = false;
    }
}

function captureImage() {
    if (isStreaming) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL('image/jpeg');
        socket.emit('image', dataURL);
    }
}

const socket = io();
socket.on('connect', () => {
    console.log('Connected to server');
    startStreaming();
});
socket.on('disconnect', () => {
    console.log('Disconnected from server');
    stopStreaming();
});
socket.on('count', (count) => {
    const message = `Number of people: ${count}`;
    document.getElementById('message').textContent = message;
});

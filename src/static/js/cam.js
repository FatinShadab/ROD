document.addEventListener('DOMContentLoaded', function() {
    // Get references to elements
    const form = document.getElementById('camRegForm');
    const regButton = document.getElementById('regBtn');
    const video = document.getElementById('video_stream');
    const testLinks = document.querySelectorAll('.test-link');
    const stopBtn = document.getElementById('stopBtn');
    const webCamTestLink = document.getElementById('text-web-cam');
    const video_placeholder = document.getElementById('video_stream_placeholder');
    const img = document.createElement('img');
    var ipCamUrl = "http://ip:port/shot.jpg?"; // Replace with your IP camera URL
    let camStream;
    let socket;
    let apiCall;

    async function startWebcam() {
        try {
            document.getElementById('camera-name').textContent = "Device Cam";
            camStream = await navigator.mediaDevices.getUserMedia({ video: true });

            setupSocket();
            setupVideo();
            startSendingFrames();
        } catch (error) {
            console.error("Error accessing webcam: ", error);
            alert("Failed to access webcam. Please check your browser settings and permissions.");
        }
    }

    function setupSocket() {
        socket = new WebSocket('ws://localhost:8000/camera/ws/video/');
        socket.onopen = () => console.log("WebSocket connection opened");
        socket.onerror = (error) => console.error("WebSocket error: ", error);
        socket.onclose = () => console.log("WebSocket connection closed");
        socket.onmessage = handleSocketMessage;
    }

    function setupVideo() {
        video.srcObject = camStream;
        video.hidden = false;
        video_placeholder.hidden = true;
        stopBtn.disabled = false;
        webCamTestLink.disabled = true;
    }

    function handleSocketMessage(event) {
        const arrayBuffer = event.data;
        const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });
        video.src = URL.createObjectURL(blob);
    }

    function startSendingFrames() {
        apiCall = setInterval(async () => {
            try {
                const frame = await grabFrame();
                const canvas = document.createElement('canvas');
                canvas.width = frame.width;
                canvas.height = frame.height;
                const context = canvas.getContext('2d');
                context.drawImage(frame, 0, 0, frame.width, frame.height);
                canvas.toBlob(sendBlob, 'image/jpeg');
            } catch (error) {
                console.error("Error capturing frame: ", error);
            }
        }, 50); // Send a frame every 50ms
    }

    async function grabFrame() {
        const imageCapture = new ImageCapture(camStream.getVideoTracks()[0]);
        return await imageCapture.grabFrame();
    }

    function sendBlob(blob) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            console.log(blob);
            socket.send(blob);
        }
    }

    function stopCam() {
        if (camStream) {
            camStream.getTracks().forEach(track => track.stop());
            camStream = null;
            video.srcObject = null;
            video.src = "!#";
        }
        if (socket) socket.close();
        if (apiCall) clearInterval(apiCall);
        video.hidden = true;

        if (!video_placeholder.hidden) {
            video_placeholder.src = "{% static '/asset/images/no_camera.jpg' %}";
        }

        video_placeholder.hidden = false;
        stopBtn.disabled = true;
        webCamTestLink.disabled = false;
        document.getElementById('camera-name').textContent = "--";
        document.getElementById('camera-ip').textContent = "--";
        document.getElementById('camera-port').textContent = "--";
    }

    async function fetchImageAsBlob(url) {
        const response = await fetch(url, { mode: 'cors' });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.blob();
    }

    async function startVideoStream(cameraData) {
        stopBtn.disabled = false;
        webCamTestLink.disabled = true;
        ipCamUrl = ipCamUrl.replace("ip", cameraData.ip);
        ipCamUrl = ipCamUrl.replace("port", cameraData.port);
        img.src = ipCamUrl;
        img.onerror = function() {
            console.log(video.error);
            alert("Failed to load video stream. Please check if the camera is online and the IP address/port is correct.");
        };

        socket = new WebSocket('ws://localhost:8000/camera/ws/video/');

        socket.onopen = function(event) {
            console.log('WebSocket is connected.');
        };

        socket.onmessage = function(event) {
            const blob = new Blob([event.data], {type: 'image/jpeg'});
            const url = URL.createObjectURL(blob);
            video_placeholder.src = url;
        };

        socket.onerror = function(error) {
            console.log('WebSocket Error: ', error);
        };

        socket.onclose = function(event) {
            console.log('WebSocket is closed now.');
            clearInterval(apiCall);
        };

        apiCall = setInterval(async () => {
            try {
                const blob = await fetchImageAsBlob(img.src);
                sendBlob(blob);
            } catch (error) {
                console.error('Error fetching image as blob:', error);
            }
        }, 50);

        // Update the testing card with camera data
        document.getElementById('camera-name').textContent = cameraData.name;
        document.getElementById('camera-ip').textContent = cameraData.ip;
        document.getElementById('camera-port').textContent = cameraData.port;
    }

    // Event listener for form input changes
    form.addEventListener('input', function() {
        const allFieldsFilled = Array.from(form.querySelectorAll('input[type="text"], input[type="number"]')).every(input => input.value.trim() !== '');
        regButton.disabled = !allFieldsFilled;
    });

    // Event listener for test links
    testLinks.forEach(function(testLink) {
        testLink.addEventListener('click', function(event) {
            event.preventDefault();
            const cameraRow = event.target.closest('tr');
            const cameraData = {
                name: cameraRow.dataset.cameraName,
                ip: cameraRow.dataset.cameraIp,
                port: cameraRow.dataset.cameraPort
            };
            startVideoStream(cameraData);
        });
    });

    // Event listener for stop button
    stopBtn.addEventListener('click', function(event) {
        stopCam();
    });

    // Event listener for webcam test link
    webCamTestLink.addEventListener('click', function(event) {
        event.preventDefault();
        stopCam();
        startWebcam();
    });
});
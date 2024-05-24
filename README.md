# R.O.D : Real-Time Object Detection
> A prototype of IP Camera video stream integration with Django Backend utilizing yolo, django channel technologies, providing real-time surveillance solution, empowering seamless object detection and monitoring.
## Table of Contents
- [Overview](#overview)
- [Learning Outcomes](#learning-outcomes)
- [Technologies Used](#technologies-used)
- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [Detailed Explanation](#detailed-explanation)
  - [IP Camera Integration](#ip-camera-integration)
  - [WebSocket Communication](#websocket-communication)
  - [YOLO Object Detection [Todo]](#yolo-object-detection)
  - [Frontend Design](#frontend-design)
 - [License](#license)

## Overview
This project demonstrates how to integrate an IP camera with a Django backend to stream video, perform object detection using YOLO, and update the frontend with processed frames. The application leverages Django Channels and Redis for WebSocket communication to ensure real-time data flow between the client and the server.

## Learning Outcomes
Through this project, I have learned:
- How to integrate an IP camera with a Django backend.
- How to establish a stable connection between the IP camera stream and the Django backend.
- The usage of Django Channels and Redis for handling WebSocket communication.
- Designing a responsive frontend using HTML and Bootstrap.
- Implementing YOLO for object detection and counting.

## Technologies Used
- **Django**: Web framework for building the backend.
- **Django Channels**: For handling WebSocket communication.
- **Redis**: Message broker used with Django Channels.
- **HTML/CSS**: For structuring and styling the frontend.
- **Bootstrap**: For frontend design.
- **JavaScript**: For client-side functionality and WebSocket management.
- **OpenCV**: For video processing.
- **YOLO**: For object detection.

## Project Setup

### Prerequisites
- Python 3.x
- Redis server
- Django 3.x or higher

### Installation
1. **Clone the repository:**
    ```bash
    git clonehttps://github.com/FatinShadab/ROD.git
    cd ROD
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
4. ** Configure Gmail SMTP Server:**
- update the 'host_email_config.json' file located in 'src/core' folder
    ```json
    {
    "EMAIL_HOST_USER": "gmail address which has app for less secure access",
    "EMAIL_HOST_PASSWORD": "app-password"
    }
    ```

5. **Start the Redis server:**
    ```bash
    docker run -p 6379:6379 -d redis:5
    ```

5. **Apply database migrations:**
    ```bash
    cd ./src/
    python manage.py migrate
    ```

7. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

### Running the Project
1. **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```

2. **Access the application in your browser:**
    ```
    http://127.0.0.1:8000
    ```

## Detailed Explanation

### IP Camera Integration
To integrate the [IP camera](https://play.google.com/store/apps/details?id=com.pas.webcam&pcampaignid=web_share), we use the camera's video feed URL and stream it in an HTML `img` tag. JavaScript captures frames from this stream and sends them to the Django backend via WebSocket for processing.

### WebSocket Communication
WebSocket communication is established using Django Channels. This allows real-time, bi-directional communication between the frontend and backend. We use Redis as the message broker to handle WebSocket messages.

### YOLO Object Detection
[Todo]: For object detection, YOLO (You Only Look Once) is implemented on the server-side. When frames are received from the frontend, YOLO processes these frames to detect and count objects. The processed frames are then sent back to the frontend via WebSocket.

### Frontend Design
The frontend is designed using HTML and Bootstrap. The user can register IP cameras, view the live stream, and see the object detection results in real-time. JavaScript is used to handle WebSocket communication and update the DOM with processed frames.

### User Authentication & Data handling
The application includes a comprehensive user authentication system, ensuring secure access to the IP camera streams and related functionalities. Here's an overview of the implemented features:

#### User Authentication
- Registration: Users can create an account by providing their email and password. An email verification step can be added for additional security.
- Login: Registered users can log in using their credentials. Django's built-in authentication system handles session management and password hashing.
- Logout: Users can securely log out of their accounts.
- Forgot Password: If a user forgets their password, they can request a password reset. An email with a reset link is sent to their registered email address. The user can then set a new password using the link.

#### Data Handling
- IP Camera Data Storage: Registered IP camera details (such as name, IP address, and port) are saved in the database. This allows users to manage their cameras from the frontend.
- User-Specific Data: Each user's camera data is associated with their account, ensuring that users can only access and manage their own cameras.

## Conclusion
This project combines several technologies to achieve real-time video processing and object detection. By integrating an IP camera with a Django backend, leveraging WebSocket communication, and using YOLO for object detection, we can build a powerful application that processes live video streams and updates the frontend in real-time.

## License
This project is under [MIT Licencse](https://github.com/FatinShadab/ROD/blob/main/LICENSE)
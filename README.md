## Run the Model Locally and Access by API

- Clone the git repo in a folder
- open the folder in VS code
- Open Terminal and type  ‘cd Backend’ → now Run the API by command
- uvicorn api:app --reload : This will Start the API at the Port 8000.
- Now the API can be called from the url : [localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000/](http://127.0.0.1:5500/)
- Next step is to run the Frontend index.html.
- Host the index.html file from Live server(VS code) or Open it for the File Manager.
- It will ask to Allow the Camera.
- And Now the Frontend will capture frame send to backend and it will be processed by the Model API.
## File Structure

```docker
.
├── Frontend/
│   └── index.html
└── Backend/
    ├── api.py
    ├── model_loader.py
    ├── Dockerfile
    └── Requirement.txt
```
### **Hand Gesture Detection: A Production-Ready ML Deployment**

Hand Gesture Detection is a fully implemented, deployment-ready project designed for real-time hand sign recognition using **MediaPipe, OpenCV, and FastAPI**. While millions of machine learning (ML) projects are developed every year, only a few progress beyond the experimentation phase in Jupyter Notebooks or VS Code to real-world deployment. This project goes beyond just writing code—it focuses on **deploying an ML model to the cloud** and optimizing its performance for practical use.

### **Deploying the ML Model to the Cloud**

A key challenge in deploying ML models, especially for **image processing and real-time detection**, is minimizing **latency**. We explored various methods to optimize communication between the client and server. Among them, encoding and decoding images into **Base64 format** and transmitting them as **JSON over HTTP or HTTPS** proved to be **more efficient** than using WebSocket connections.

### **Why Not WebSockets?**

WebSocket connections establish a persistent link between the client and server, but they come with **higher resource consumption and increased latency**. Additionally, WebSocket-based implementations require a dedicated backend service to **manage and maintain connections** between clients and servers.

Instead, by using **RESTful API endpoints**, we eliminate the need for a **master controller backend server**. The system only requires an **ML model API** and a **model loader**, reducing complexity while ensuring scalability. When deployed on the cloud, **load balancers** provided by cloud service providers further enhance performance by distributing requests efficiently across multiple instances.

### **How the System Works**

1. **Image Encoding & Transmission:**
    - The client encodes the image into a **JPEG binary blob** and sends it to the server over HTTP.
2. **Server Processing:**
    - The server receives the binary data, **decodes it back into an image**, and processes it using the ML model.
    - The model analyzes the image, detects the hand gesture, and adds **annotations**.
3. **Response to Client:**
    - The processed image is **converted into a Base64-encoded JSON** file.
    - The server sends this JSON response back to the client.
4. **Client-Side Decoding & Display:**
    - The client decodes the Base64 JSON back into an image and displays it to the user with **gesture annotations**.

This approach ensures **low latency, minimal resource consumption, and scalable deployment** of the hand gesture detection model in the cloud. By leveraging **REST APIs and Base64 encoding**, we eliminate the complexity of maintaining WebSocket connections, making the system more **efficient, cost-effective, and production-ready**.

## Implementing in AWS [link]
## full detailed report [link]

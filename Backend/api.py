import os
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from model_loader import HandGestureRecognizer  # Assuming HandGestureRecognizer is in this file

# Suppress TensorFlow and oneDNN warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the gesture recognizer once
gesture_recognizer = HandGestureRecognizer()

# Endpoint to check the API status
@app.get("/")
def read_root():
    return {"message": "Hand Gesture Recognition API is running!"}

# Endpoint for uploading an image and recognizing gestures
@app.post("/recognize-gesture/")
async def recognize_gesture(file: UploadFile = File(...)):
    # Check if the uploaded file is an image
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Upload a JPEG or PNG image.")
    
    # Read the image file
    contents = await file.read()
    np_array = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    if image is None:
        raise HTTPException(status_code=400, detail="Unable to read the image file.")
    
    # Convert the image to RGB for MediaPipe processing
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = gesture_recognizer.hands.process(image_rgb)
    
    gestures = []
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Recognize the gesture
            gesture = gesture_recognizer.recognize_gesture(hand_landmarks)
            gestures.append(gesture)
            
            # Draw landmarks on the image
            gesture_recognizer.mp_drawing.draw_landmarks(
                image, hand_landmarks, 
                gesture_recognizer.mp_hands.HAND_CONNECTIONS
            )
    
    # Encode the processed image as a Base64 string
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode("utf-8")
    
    return JSONResponse(content={
        "gestures": gestures,
        "processed_image": image_base64
    })

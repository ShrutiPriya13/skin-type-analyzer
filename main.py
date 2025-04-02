from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from fastapi.middleware.cors import CORSMiddleware
from recommendations.recommend import recommend_products  # Ensure this function is correct
from typing import List, Dict

app = FastAPI()

# Load the trained skin type detection model
model = tf.keras.models.load_model("skin_type_model.h5")  # Update path if needed

# Define class labels
CLASS_LABELS = ["Oily Skin", "Dry Skin", "Combination Skin", "Normal Skin", "Sensitive Skin"]

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class QuestionnaireInput(BaseModel):
    skin_feel: int
    breakout_frequency: int
    tight_flaky: int
    pores: int
    sun_reaction: int

@app.post("/predict_questionnaire/")
def predict_questionnaire(data: QuestionnaireInput):
    # Dummy logic for prediction (replace with your model)
    if data.skin_feel == 3:
        skin_type = "Normal"
    elif data.skin_feel == 2:
        skin_type = "Combination"
    else:
        skin_type = "Oily"
        
    recommended_products = recommend_products(skin_type)

    if not recommended_products:
        recommended_products = [{"product_name": "No recommendations available", "product_url": "", "price": ""}]

    return {"skin_type": skin_type, "recommended_products": recommended_products}

@app.post("/predict/")
async def predict_skin_type(file: UploadFile = File(...)):
    """Predicts skin type from an uploaded image."""
    try: 
        # Read image file
        image = Image.open(io.BytesIO(await file.read()))
        image = image.resize((224, 224))  # Resize to match model input shape
        image = np.array(image) / 255.0  # Normalize pixel values
        image = np.expand_dims(image, axis=0)  # Expand dimensions for model input

        # Make prediction
        predictions = model.predict(image)
        predicted_class = np.argmax(predictions)
        confidence = float(np.max(predictions))  # Get confidence score

        # Get skin type
        skin_type = CLASS_LABELS[predicted_class]

        # Fetch product recommendations
        recommended_products = recommend_products(skin_type)

        return {
            "skin_type": skin_type,
            "confidence": confidence,
            "recommended_products": recommended_products  # Use CSV-based recommendations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in prediction: {str(e)}")

@app.get("/recommend/{skin_type}")
def get_recommendations(skin_type: str):
    """
    Get recommended skincare products based on the skin type.
    """
    # Fix spaces in skin_type
    skin_type = skin_type.replace("%20", " ")

    recommended_products = recommend_products(skin_type)

    if not recommended_products:  # Ensure empty lists return 404
        raise HTTPException(status_code=404, detail="No recommendations found for this skin type.")

    # Ensure the response structure is correct
    return {
        "skin_type": skin_type,
        "recommended_products": [
            {
                "product_name": product["product_name"],
                "product_url": product["product_url"],
                "price": product["price"]
            }
            for product in recommended_products
        ]
    }

### ROOT ENDPOINT ###
@app.get("/")
def home():
    return {"message": "Welcome to the Skin Type Detection API!"}


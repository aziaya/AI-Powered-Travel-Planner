from fastapi import FastAPI, HTTPException
from app.models import TravelGuideInput, TravelGuideOutput
from app.services import generate_travel_guide, stream_travel_response
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/generate-travel-guide", response_model=TravelGuideOutput)
async def generate_travel_guide_endpoint(input_data: TravelGuideInput):
    try:
        logger.info(f"Generating travel guide for destinations: {input_data.destinations}")
        guide = generate_travel_guide(
            destinations=input_data.destinations,
            travel_dates=input_data.travel_dates,
            interests=input_data.interests,
            user_budget=input_data.user_budget,
            number_of_travellers=input_data.number_of_travellers
        )
        return guide
    except Exception as e:
        logger.error(f"Error generating travel guide: {e}")
        raise HTTPException(status_code=500, detail=str(e))






# WebSocket endpoint for streaming travel-related responses
@app.websocket("/ws/travel-chat")
async def websocket_travel_chat(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        while True:
            # Receive the user's prompt
            prompt = await websocket.receive_text()
            logger.info(f"Received prompt: {prompt}")

            # Stream the response in real-time
            await stream_travel_response(websocket, prompt)
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"Error in WebSocket communication: {e}")
        await websocket.close(code=1011)  # Internal server error
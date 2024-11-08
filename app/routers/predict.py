from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from app.services import yolo_service, ocr_service
from app.utils.auth import get_api_key
import logging

router = APIRouter()

@router.post("/predict", response_class=PlainTextResponse, dependencies=[Depends(get_api_key)])
async def predict_endpoint(file: UploadFile = File(...)):
    logger = logging.getLogger("app")
    try:
        logger.info("Request received for /predict")
        results, boxes, image = await yolo_service.predict(file)
        response_text = await ocr_service.recognize_text(results, boxes, image, idx_to_char)
        logger.info(f"Response: {response_text}")
        return response_text
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

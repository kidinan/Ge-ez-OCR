from fastapi import FastAPI
from app.routers import predict
from app.utils.logging import setup_logging
from app.utils.auth import get_api_key

# Setup logging
logger = setup_logging()

app = FastAPI()

# Include the prediction router
app.include_router(predict.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")

import uvicorn
from app.core.config import API_PORT

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app", host="0.0.0.0", port=API_PORT, reload=True, log_level="info"
    )

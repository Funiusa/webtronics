import uvicorn
from config import API_PORT

if __name__ == "__main__":
    uvicorn.run(
        "app.api:app", host="0.0.0.0", port=API_PORT, reload=True, log_level="info"
    )

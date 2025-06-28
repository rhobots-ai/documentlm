"""Health check endpoints."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    """Health check endpoint.
    
    Returns:
        Response: Health status response
    """
    # Use the same format as Flask
    return JSONResponse(content={"status": "ready"})

"""
Main API entry point for the DocumentLM FastAPI application.

This file is a wrapper around the modular API implementation in the api/ directory.
It provides compatibility with existing deployment scripts and server configurations.
"""

# This should be left for uvicorn and direct CLI execution
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)

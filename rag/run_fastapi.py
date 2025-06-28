"""
Run the FastAPI application for development.

This script is used to run the FastAPI application in development mode.

Examples:
    # Run on default port 5000
    python run_fastapi.py
    
    # Run on a specific port
    python run_fastapi.py --port 8080
    
    # Run with auto-reload enabled
    python run_fastapi.py --reload
    
    # Run on localhost only
    python run_fastapi.py --host 127.0.0.1
"""
import argparse
import uvicorn


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the FastAPI application")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5001, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    print(f"Starting FastAPI server on {args.host}:{args.port}")
    print(f"API Documentation available at: http://localhost:{args.port}/docs")
    print("Ctrl+C to stop the server")
    
    uvicorn.run(
        "api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )

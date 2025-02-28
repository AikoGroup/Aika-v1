"""
Command-line interface for the Aika AI System.
"""

import argparse
import sys
from typing import List, Optional

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code
    """
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(
        description="Aika AI System - Insurance platform orchestration system"
    )
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start the Aika API server")
    start_parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0", 
        help="Host to bind the server to"
    )
    start_parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to"
    )
    start_parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    # Parse arguments
    parsed_args = parser.parse_args(args)
    
    # Handle commands
    if parsed_args.command == "start":
        return start_server(
            host=parsed_args.host,
            port=parsed_args.port,
            reload=parsed_args.reload
        )
    elif parsed_args.command == "version":
        return show_version()
    else:
        parser.print_help()
        return 1

def start_server(host: str, port: int, reload: bool) -> int:
    """
    Start the Aika API server.
    
    Args:
        host: Host to bind the server to
        port: Port to bind the server to
        reload: Whether to enable auto-reload
        
    Returns:
        Exit code
    """
    try:
        import uvicorn
        print(f"Starting Aika API server on {host}:{port}")
        uvicorn.run(
            "src.api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        return 0
    except ImportError:
        print("Error: uvicorn is not installed. Please install it with 'pip install uvicorn'.")
        return 1
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1

def show_version() -> int:
    """
    Show version information.
    
    Returns:
        Exit code
    """
    from src import __version__
    print(f"Aika AI System v{__version__}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

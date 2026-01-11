#!/usr/bin/env python3
"""
Direct VoiceMode converse wrapper for OpenCode.

This script provides zero-latency voice conversation by calling VoiceMode
tools directly without MCP server overhead.
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Ensure VoiceMode is importable
try:
    import voice_mode
except ImportError:
    print("Error: VoiceMode package not installed.", file=sys.stderr)
    print("Run: uvx voice-mode-install --yes", file=sys.stderr)
    sys.exit(1)

from voice_mode.config import setup_logging
from voice_mode.core import cleanup as cleanup_clients

# Set up logging
logger = setup_logging()


def main():
    """Main entry point for direct voice conversation."""
    parser = argparse.ArgumentParser(
        description="Start a voice conversation with VoiceMode (OpenCode integration)"
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Initial message to speak (optional)",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't wait for response (speak only)",
    )
    parser.add_argument(
        "--voice",
        help="TTS voice to use (e.g., alloy, nova, shimmer)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Maximum recording duration in seconds",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output",
    )
    
    args = parser.parse_args()
    
    # Set debug mode
    if args.debug:
        logging.getLogger("voicemode").setLevel(logging.DEBUG)
    
    # Join message parts
    initial_message = " ".join(args.message) if args.message else None
    
    try:
        # Import converse function
        import asyncio
        from voice_mode.tools.converse import converse
        
        # Prepare parameters
        kwargs = {
            "wait_for_response": not args.no_wait,
        }
        
        if args.voice:
            kwargs["voice"] = args.voice
        
        if args.duration:
            kwargs["listen_duration_max"] = args.duration
        
        # Call converse (it's async, so we need to run it)
        result = asyncio.run(converse(
            message=initial_message or "Hello! How can I help you?",
            **kwargs
        ))
        
        # Print result - the function returns a string directly
        if result:
            print(result)
        
    except Exception as e:
        logger.error(f"Voice conversation failed: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    finally:
        # Clean up resources
        try:
            cleanup_clients()
        except Exception as e:
            logger.warning(f"Cleanup warning: {e}")


if __name__ == "__main__":
    main()

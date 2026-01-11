#!/usr/bin/env python3
"""
Direct VoiceMode service status wrapper for OpenCode.

Provides service status information without MCP server.
"""

import sys
import asyncio
from pathlib import Path

# Ensure VoiceMode is importable
try:
    import voice_mode
except ImportError:
    print("Error: VoiceMode package not installed.", file=sys.stderr)
    print("Run: uvx voice-mode-install --yes", file=sys.stderr)
    sys.exit(1)

from voice_mode.tools.service import service


async def check_all_services():
    """Check status of all VoiceMode services."""
    
    services = ["whisper", "kokoro"]
    
    print("\nVoiceMode Services Status")
    print("━" * 50)
    print()
    
    all_healthy = True
    
    for service_name in services:
        try:
            result = await service(
                service_name=service_name,
                action="status"
            )
            
            # The service function returns a formatted string
            print(result)
            print()
            
            # Check if service is running from the result
            if "not running" in result.lower() or "error" in result.lower():
                all_healthy = False
        
        except Exception as e:
            print(f"{service_name.capitalize()}:")
            print(f"  Status: ❌ Error")
            print(f"  Info:   {str(e)}")
            print()
            all_healthy = False
    
    # Summary
    if all_healthy:
        print("✅ All services healthy")
        return 0
    else:
        print("⚠️  Some services need attention")
        print()
        print("To start services, run:")
        print("  voicemode service start whisper")
        print("  voicemode service start kokoro")
        return 1


def main():
    """Main entry point."""
    return asyncio.run(check_all_services())


if __name__ == "__main__":
    sys.exit(main())

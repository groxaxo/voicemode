#!/usr/bin/env python3
"""
Direct VoiceMode service status wrapper for OpenCode.

Provides service status information without MCP server.
"""

import sys
import json
from pathlib import Path

# Ensure VoiceMode is importable
try:
    import voice_mode
except ImportError:
    print("Error: VoiceMode package not installed.", file=sys.stderr)
    print("Run: uvx voice-mode-install --yes", file=sys.stderr)
    sys.exit(1)

from voice_mode.tools.service import service_impl


def main():
    """Check status of all VoiceMode services."""
    
    services = ["whisper", "kokoro", "livekit"]
    
    print("\nVoiceMode Services Status")
    print("━" * 50)
    print()
    
    all_healthy = True
    
    for service_name in services:
        try:
            result = service_impl(
                service_name=service_name,
                action="status"
            )
            
            if result.get("error"):
                print(f"{service_name.capitalize()}:")
                print(f"  Status: ❌ Error")
                print(f"  Info:   {result['error']}")
                all_healthy = False
            else:
                status = result.get("status", {})
                is_running = status.get("running", False)
                
                print(f"{service_name.capitalize()}:")
                if is_running:
                    print(f"  Status: ✅ Running")
                    if status.get("port"):
                        print(f"  Port:   {status['port']}")
                    if status.get("pid"):
                        print(f"  PID:    {status['pid']}")
                else:
                    print(f"  Status: ⚠️  Not running")
                    all_healthy = False
                
                # Show health status if available
                if status.get("health"):
                    health = status["health"]
                    if health == "healthy":
                        print(f"  Health: Healthy")
                    elif health == "degraded":
                        print(f"  Health: ⚠️  Degraded")
                        all_healthy = False
                    else:
                        print(f"  Health: ❌ Unhealthy")
                        all_healthy = False
            
            print()
        
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


if __name__ == "__main__":
    sys.exit(main())

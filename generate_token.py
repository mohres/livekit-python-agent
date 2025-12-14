#!/usr/bin/env python3
"""
Generate a LiveKit room token for testing in the playground.
"""

import os
from livekit import api
from dotenv import load_dotenv

def generate_token(room_name: str = "test-room", participant_name: str = "user"):
    """Generate a room token for the LiveKit playground."""

    # Load environment variables
    load_dotenv()

    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    livekit_url = os.getenv("LIVEKIT_URL")

    if not all([api_key, api_secret, livekit_url]):
        print("❌ Error: Missing required environment variables in .env")
        print("Required: LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL")
        return None

    # Create access token
    token = api.AccessToken(api_key, api_secret) \
        .with_identity(participant_name) \
        .with_name(participant_name) \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        ))

    jwt_token = token.to_jwt()

    print("🎉 LiveKit Token Generated Successfully!")
    print(f"📍 Room: {room_name}")
    print(f"👤 Participant: {participant_name}")
    print(f"🔗 LiveKit URL: {livekit_url.replace('wss://', '').replace('ws://', '')}")
    print(f"🎫 Token: {jwt_token}")
    print()
    print("📋 How to use in playground:")
    print("1. Go to: https://agents-playground.livekit.io")
    print(f"2. Enter URL: {livekit_url.replace('wss://', '').replace('ws://', '')}")
    print(f"3. Enter Token: {jwt_token}")
    print("4. Click Connect and start talking!")

    return jwt_token

if __name__ == "__main__":
    import sys

    room = sys.argv[1] if len(sys.argv) > 1 else "test-room"
    participant = sys.argv[2] if len(sys.argv) > 2 else "user"

    generate_token(room, participant)
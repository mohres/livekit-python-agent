#!/usr/bin/env python3

import asyncio
import logging
import signal
import sys
from typing import Optional

from livekit.agents import (
    Agent,
    AgentServer,
    JobContext,
    cli,
    voice
)
from livekit.plugins.silero import VAD
from livekit import rtc
from livekit.plugins.google.realtime import RealtimeModel
from livekit.plugins import liveavatar

from src.config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global config
config = get_config()

# Create agent server
server = AgentServer()

@server.rtc_session(agent_name=config.agent.name)
async def agent_entrypoint(ctx: JobContext) -> None:
    """
    Main agent entry point using modern LiveKit RealtimeModel for Gemini Live API.
    """
    logger.info(f"Agent {config.agent.name} starting in room: {ctx.room.name}")

    avatar_session = None

    try:
        # Create Gemini Live API model
        gemini_model = RealtimeModel(
            api_key=config.gemini.api_key,
            model=config.gemini.model,  # Use configured model
            voice=config.gemini.voice,  # Available voices: Puck, Charon, Kore, Fenrir, Aoede
            instructions=config.agent.instructions,
            modalities=["AUDIO"],  # Audio-only mode
            temperature=config.gemini.temperature  # Use configured temperature
        )

        # Create Agent instance with instructions
        agent = Agent(instructions=config.agent.instructions)

        # Create agent session with Gemini Live API
        agent_session = voice.AgentSession(
            vad=VAD.load(),  # Use Silero VAD for interruption
            llm=gemini_model  # Direct LLM integration
        )

        # Setup LiveAvatar integration if configured
        if config.liveavatar.api_key and config.liveavatar.avatar_id:
            try:
                avatar_session = liveavatar.AvatarSession(
                    avatar_id=config.liveavatar.avatar_id,
                    api_key=config.liveavatar.api_key
                )
                logger.info(f"LiveAvatar session created with avatar ID: {config.liveavatar.avatar_id}")
            except Exception as e:
                logger.warning(f"Failed to create LiveAvatar session (will continue without avatar): {e}")
                avatar_session = None
        else:
            logger.info("LiveAvatar not configured, continuing with audio-only mode")

        # Set up room event handlers
        @ctx.room.on("participant_connected")
        def on_participant_connected(participant: rtc.RemoteParticipant):
            logger.info(f"Participant connected: {participant.identity}")

        @ctx.room.on("participant_disconnected")
        def on_participant_disconnected(participant: rtc.RemoteParticipant):
            logger.info(f"Participant disconnected: {participant.identity}")

        # Start the agent session
        if avatar_session:
            # Try to start with LiveAvatar, fallback to audio-only on failure
            try:
                await avatar_session.start(agent_session, room=ctx.room)
                logger.info("Agent started with LiveAvatar integration")
            except Exception as e:
                logger.warning(f"Failed to start with LiveAvatar (continuing without avatar): {e}")
                await agent_session.start(agent=agent, room=ctx.room)
                logger.info("Agent started in audio-only mode after LiveAvatar failure")
        else:
            # Start without avatar
            await agent_session.start(agent=agent, room=ctx.room)
            logger.info("Agent started in audio-only mode")

        logger.info(f"Agent {config.agent.name} started successfully")

    except Exception as e:
        logger.error(f"Error in agent entrypoint: {e}")
        raise
    finally:
        # Cleanup is handled automatically by LiveKit agents framework
        logger.info("Agent session cleanup completed")

def main():
    """Main entry point for running the agent."""
    try:
        # Set up signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            logger.info("Received shutdown signal, stopping agent...")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        logger.info(f"Starting {config.agent.name} with LiveAvatar integration...")

        # Run the agent server
        cli.run_app(server)

    except KeyboardInterrupt:
        logger.info("Agent stopped by user")
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
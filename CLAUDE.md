# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LiveKit Python agent that provides multi-modal voice AI functionality with Google Gemini Live API integration and optional LiveAvatar support. The agent is configured as "Aram", a Saudi Arabic-speaking hotel guest relations assistant for Mecca hotels.

## Architecture

### Core Components

- **agent.py**: Main entry point with pre-warm capability for faster startup
- **config.py**: Configuration management with dataclasses for all service settings
- **handlers/voice_handler.py**: Orchestrates conversation flow using LiveKit AgentSession
- **handlers/gemini_handler.py**: Google Gemini Live API integration for real-time audio processing
- **LiveAvatar Integration**: Uses official `livekit-plugins-liveavatar` plugin for visual representation

### Voice Processing Flow
```
LiveKit Room → Voice Handler → Gemini Handler → Audio Response
      ↓                ↓
   Avatar Session ← Audio Routing
```

### Pre-warm Pattern
Following TypeScript playground agent patterns:
- Voice handler is initialized during agent startup (not when user joins)
- Gemini model is pre-configured for faster first response
- Uses global `_prewarmed_handler` variable to cache initialized handler

## Development Commands

### Environment Setup
```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials

# Install dependencies
uv sync
```

### Running the Agent
```bash
# Development mode with file watching
uv run python -m src.agent dev

# Console mode for testing
uv run python -m src.agent console

# Production mode
uv run python -m src.agent start
```

### Testing

#### Unit Tests
```bash
# Run all tests (if test files exist)
uv run pytest

# Run specific test file
uv run pytest tests/test_filename.py

# Run with coverage
uv run pytest --cov=src
```

#### Avatar Testing
1. **Start agent**: `uv run python -m src.agent dev`
2. **Open playground**: https://agents-playground.livekit.io
3. **Connect using your LiveKit URL** from `.env`
4. **Join any room** and interact with the Arabic-speaking avatar
5. **Expected behavior**: Avatar shows lip-sync, gestures, and responds in Saudi Arabic

## Configuration Management

### Required Environment Variables
- `LIVEKIT_URL`: WebSocket URL for LiveKit server
- `LIVEKIT_API_KEY` & `LIVEKIT_API_SECRET`: LiveKit credentials
- `GEMINI_API_KEY`: Google Gemini API key

### Optional Configuration
- `GEMINI_MODEL`: Default is "gemini-2.5-flash-native-audio-preview-09-2025"
- `GEMINI_VOICE`: Default is "Enceladus"
- `GEMINI_TEMPERATURE`: Default is 0.2 for optimized speed
- `LIVEAVATAR_API_KEY` & `AVATAR_ID`: For visual avatar integration
- `AGENT_NAME`: Default is "Aram Voice Assistant"
- `ROOM_PREFIX`: Default is "call-"

### Agent Personality
The agent is configured in Arabic for hotel guest relations:
- **Language**: Saudi Arabic exclusively
- **Role**: Guest relations at Mecca hotel
- **Capabilities**: Hotel services, prayer times, local directions, concierge services

## Key Technical Details

### Audio Optimization
- Sample Rate: 16kHz mono
- Echo Cancellation: Enabled
- Auto Gain Control: Enabled
- Latency Hint: Interactive for real-time conversations
- Interruption Threshold: 0.2 for natural conversation flow

### Voice Activity Detection
- Uses Silero VAD for interruption handling
- Configured for telephony-optimized detection

### Session Management
- AgentSession manages the conversation lifecycle
- Custom LLM adapter bridges AgentSession with Gemini
- Proper resource cleanup in try/finally blocks

## LiveAvatar Integration

Optional visual representation that:
- Joins as separate room participant
- Routes audio through avatar for lip-sync
- Supports emotions and gestures
- Requires `LIVEAVATAR_API_KEY` and `AVATAR_ID` environment variables

## Common Development Patterns

### Adding New Handlers
1. Create handler in `src/handlers/`
2. Implement initialization and cleanup methods
3. Integrate with VoiceHandler in the main conversation flow
4. Update config.py if new environment variables needed

### Error Handling
- Use structured logging with logger.error() for exceptions
- Implement proper resource cleanup in finally blocks
- Pre-warm handler gracefully handles initialization failures

### Configuration Changes
- Add new config dataclasses in config.py
- Update get_config() function with environment variable loading
- Use default values for optional configurations
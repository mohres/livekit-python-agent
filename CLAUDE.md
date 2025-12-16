# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LiveKit Python agent that provides multi-modal voice AI functionality with Google Gemini Live API integration and optional avatar support (Tavus or LiveAvatar). The agent is configured as "Aram", a Saudi Arabic-speaking hotel guest relations assistant for Mecca hotels.

## Architecture

### Core Components

- **agent.py**: Main entry point with pre-warm capability for faster startup
- **config.py**: Configuration management with dataclasses for all service settings
- **handlers/voice_handler.py**: Orchestrates conversation flow using LiveKit AgentSession
- **handlers/gemini_handler.py**: Google Gemini Live API integration for real-time audio processing
- **Avatar Integration**: Supports Tavus (recommended) or LiveAvatar plugins for visual representation

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

#### Cloud Testing (Recommended)
1. **Start agent**: `uv run python -m src.agent dev`
2. **Open playground**: https://agents-playground.livekit.io
3. **Connect using your LiveKit URL** from `.env`
4. **Join any room** and interact with the Arabic-speaking avatar
5. **Expected behavior**: Avatar shows lip-sync, gestures, and responds in Saudi Arabic

#### Official Agents Playground Testing (Recommended)

The best way to test locally is using LiveKit's official agents playground - the same interface as the cloud playground:

**Setup (one-time):**
1. **Clone the official playground** (outside your project directory):
   ```bash
   cd .. && git clone https://github.com/livekit/agents-playground.git
   ```

2. **Install dependencies**:
   ```bash
   cd agents-playground && pnpm install
   ```

3. **Configure with your LiveKit credentials**:
   ```bash
   # Create .env.local with your LiveKit settings
   cp .env.example .env.local
   # Edit .env.local with your LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET
   ```

**Testing Steps:**
1. **Start your Python agent**: `uv run python -m src.agent dev`
2. **Start the playground**: `cd ../agents-playground && pnpm run dev`
3. **Open your browser**: Navigate to `http://localhost:3000`
4. **Join a room**: Enter any room name (e.g., "test-room")
5. **Test with avatar**: The avatar video will appear and respond to your voice in Saudi Arabic
6. **Expected behavior**: Full multimodal interaction with avatar video, lip-sync, and voice

**Perfect for Avatar Testing:**
- ✅ **Avatar video display** - see your LiveAvatar in action locally
- ✅ **Audio visualization** and real-time transcription
- ✅ **Settings panel** to adjust audio/video preferences
- ✅ **Same UI as cloud playground** but running locally
- ✅ **Multimodal interface** - supports audio, video, and text input

#### Alternative: Local LiveKit Server Testing

For testing without internet dependency:

**Prerequisites:**
- Install LiveKit server: `brew install livekit`
- Or with Docker: `docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp -e LIVEKIT_DEV=1 livekit/livekit-server:latest --dev`

**Steps:**
1. **Start local LiveKit server**: `livekit-server --dev`
2. **Update `.env` for local testing**:
   ```env
   LIVEKIT_URL=ws://localhost:7880
   LIVEKIT_API_KEY=devkey
   LIVEKIT_API_SECRET=secret
   ```
3. **Start agent**: `uv run python -m src.agent dev`
4. **Use web frontend**: Update `../agent-starter-embed/.env.local` with local credentials

## Configuration Management

### Required Environment Variables
- `LIVEKIT_URL`: WebSocket URL for LiveKit server
- `LIVEKIT_API_KEY` & `LIVEKIT_API_SECRET`: LiveKit credentials
- `GEMINI_API_KEY`: Google Gemini API key

### Optional Configuration
- `GEMINI_MODEL`: Default is "gemini-2.5-flash-native-audio-preview-09-2025"
- `GEMINI_VOICE`: Default is "Enceladus"
- `GEMINI_TEMPERATURE`: Default is 0.2 for optimized speed
- `TAVUS_API_KEY` & `REPLICA_ID`: For Tavus avatar integration (recommended)
- `LIVEAVATAR_API_KEY` & `AVATAR_ID`: For LiveAvatar integration (legacy)
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

## Avatar Integration

### Tavus Integration (Recommended)

High-performance avatar provider that:
- Provides sub-second latency (<600ms)
- Supports custom replicas created from 2-minute videos
- Handles audio output directly (agent audio is disabled)
- Requires `TAVUS_API_KEY` and `REPLICA_ID` environment variables
- **Setup**: Create account at platform.tavus.io, upload training video, get replica ID
- **Cost**: Starting at $59/month + usage

### LiveAvatar Integration (Legacy)

Optional visual representation that:
- Joins as separate room participant
- Routes audio through avatar for lip-sync
- Supports emotions and gestures
- Requires `LIVEAVATAR_API_KEY` and `AVATAR_ID` environment variables
- **Note**: Custom avatars require Enterprise subscription

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
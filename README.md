# LiveKit Python Agent with Google Gemini Live API

A modern Python LiveKit agent featuring native Google Gemini Live API integration and optional LiveAvatar support for visual representation.



## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy configuration template
cp .env.example .env
```

Edit `.env` with your credentials:


### 2. Install Dependencies

```bash
uv sync
```

### 3. Run the Agent

```bash
# Development mode with file watching
uv run python -m src.agent dev

# Console mode for testing
uv run python -m src.agent console

# Production mode
uv run python -m src.agent start
```

### 4. Test with Web Frontend

#### Option A: Official LiveKit Web Frontend (Recommended)

For the best local testing experience, use LiveKit's official web frontend:

1. **Set up the official frontend** (one-time setup):
   ```bash
   # Clone the official agents playground (outside your project directory)
   cd .. && git clone https://github.com/livekit/agents-playground.git
   cd agents-playground && pnpm install

   # Configure with your LiveKit credentials
   cp .env.example .env.local
   # Edit .env.local with your LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET
   ```

2. **Test your agent with avatar**:
   ```bash
   # Terminal 1: Start your Python agent
   uv run python -m src.agent dev

   # Terminal 2: Start the agents playground
   cd ../agents-playground && pnpm run dev
   ```

3. **Interact with Aram's avatar**:
   - Open http://localhost:3000 in your browser
   - Join any room name (e.g., "test-room")
   - **Avatar video will appear** when your agent joins
   - Start speaking in Arabic to see the avatar respond with lip-sync
   - Experience the full multimodal agent with visual representation!

**Perfect for avatar testing:**
- ✅ **Avatar video display** - see your LiveAvatar in action
- ✅ **Audio visualization** and real-time transcription
- ✅ **Settings panel** to adjust audio/video preferences
- ✅ **Same UI as cloud playground** but running locally
- ✅ **Multimodal interface** - audio, video, and text input

#### Option B: LiveKit Cloud Playground
1. **Start agent**: `uv run python -m src.agent dev`
2. **Wait for**: `registered worker {"agent_name": "Aram Voice Assistant"...}`
3. **Open**: https://agents-playground.livekit.io
4. **Select your LiveKit Cloud project** from the dropdown
5. **Join any room** and start talking in Arabic or English

## 🎭 LiveAvatar Integration

To enable the visual avatar:

1. **Get LiveAvatar credentials** from https://liveavatar.com
2. **Set credentials in .env**:
   ```env
   LIVEAVATAR_API_KEY=your-api-key
   AVATAR_ID=your-avatar-id
   ```
3. **Restart the agent** - avatar will appear as a video participant
4. **Look for the avatar video stream** in the playground (512x512 video window)

### Troubleshooting LiveAvatar

- **"No credits available"**: Contact LiveAvatar support or disable avatar by leaving credentials blank
- **No video**: Check that `LIVEAVATAR_API_KEY` and `AVATAR_ID` are correctly set
- **Agent works without avatar**: This is expected behavior - audio-only mode is the fallback

## 🏗️ Architecture

### Modern Design

This implementation uses LiveKit's 2024 best practices:

```python
# Native Gemini Live API integration
gemini_model = RealtimeModel(
    api_key=config.gemini.api_key,
    voice="Puck",
    instructions=config.agent.instructions,
    modalities=["AUDIO"],
    turn_detection={"type": "SERVER_VAD"}
)

# Simple agent session creation
agent_session = voice.AgentSession(
    vad=voice.VAD.load("silero"),
    agent=voice.Agent(
        instructions=config.agent.instructions,
        llm=gemini_model
    )
)
```

### Project Structure

```
src/
├── agent.py      # Main agent entry point (modern LiveKit patterns)
└── config.py     # Configuration management
```

### Key Improvements from Previous Version

- ✅ **Removed 200+ lines** of custom integration code
- ✅ **Native LiveKit RealtimeModel** instead of custom handlers
- ✅ **Built-in audio pipeline** with automatic format conversion
- ✅ **Graceful LiveAvatar fallback** - works with or without avatar
- ✅ **Modern dependencies** using `livekit-plugins-google`
- ✅ **Simplified configuration** with clear environment variables

## 🔧 Configuration

### Agent Personality

Aram is configured as a Saudi Arabian hotel guest relations assistant:

```python
instructions = """أنت آرام، مسؤول خدمة الضيوف في فندق مكة المكرمة.
تتحدث بالعربية السعودية فقط بأسلوب مهني ومرحب.

مهامك:
- الترحيب بالضيوف وتقديم المساعدة في جميع احتياجاتهم
- تقديم معلومات عن خدمات الفندق
- مساعدة في الحجوزات والاستفسارات
- تقديم نصائح حول مكة المكرمة والمدينة المنورة
- مساعدة في أوقات الصلاة والاتجاهات"""
```

### Audio Settings

- **Sample Rate**: 16kHz mono (automatically handled by LiveKit)
- **VAD**: Silero VAD for natural conversation flow
- **Turn Detection**: Server-side VAD from Gemini Live API
- **Voice**: "Puck" (available: Puck, Charon, Kore, Fenrir, Aoede)

## 🖥️ Local Development

For local testing, we recommend using LiveKit's official web frontend (as shown above), which provides:

- Professional UI components optimized for agent interaction
- Built-in audio visualization and connection status
- Proper WebRTC handling with echo cancellation
- Real-time error handling and reconnection logic
- No custom server setup required

The official frontend automatically handles token generation and provides a much better user experience than custom playground implementations.


## 🌍 Production Deployment

### Environment Variables

```env
# Production settings
LOG_LEVEL=WARNING
AGENT_NAME=Production Aram Assistant

# Optional: Custom room prefix
ROOM_PREFIX=prod-
```

### Running in Production

```bash
# Start production agent
uv run python -m src.agent start

# With process management (systemd, supervisor, etc.)
# Create service file pointing to: uv run python -m src.agent start
```

## 📚 API Reference

### Available Modes

- `dev`: Development mode with file watching
- `console`: Console mode for testing
- `start`: Production mode

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LIVEKIT_URL` | Yes | Your LiveKit server URL |
| `LIVEKIT_API_KEY` | Yes | LiveKit API key |
| `LIVEKIT_API_SECRET` | Yes | LiveKit API secret |
| `GOOGLE_API_KEY` | Yes | Google Gemini API key |
| `AGENT_NAME` | No | Agent name (default: "Aram Voice Assistant") |
| `LIVEAVATAR_API_KEY` | No | LiveAvatar API key (optional) |
| `AVATAR_ID` | No | LiveAvatar avatar ID (optional) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

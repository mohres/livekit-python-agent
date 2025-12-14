# LiveKit Python Agent with Google Gemini Live API

A modern Python LiveKit agent featuring native Google Gemini Live API integration and optional LiveAvatar support for visual representation.

## 🎯 Features

- **Modern Architecture**: Native Google Gemini Live API integration using LiveKit's RealtimeModel
- **Audio-First Design**: Real-time voice AI with 16kHz audio processing
- **Arabic Personality**: "Aram" - Saudi Arabian hotel guest relations assistant
- **Optional LiveAvatar**: Visual avatar representation with graceful fallback
- **Production Ready**: Built with 2024 LiveKit best practices

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy configuration template
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# LiveKit Configuration (get from https://cloud.livekit.io)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Google Gemini Configuration (get from https://aistudio.google.com/app/apikey)
GOOGLE_API_KEY=your-gemini-api-key

# Agent Configuration
AGENT_NAME=Aram Voice Assistant

# LiveAvatar Configuration (Optional - leave blank to disable)
LIVEAVATAR_API_KEY=
AVATAR_ID=
```

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

### 4. Test with LiveKit Playground

1. **Start agent**: `uv run python -m src.agent dev`
2. **Wait for**: `registered worker {"agent_name": "Aram Voice Assistant"...}`
3. **Open**: https://agents-playground.livekit.io
4. **Connect using your LiveKit URL** from `.env` (remove `wss://` prefix)
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

## 🚨 Troubleshooting

### Connection Issues

```bash
# Check agent logs for errors
uv run python -m src.agent dev

# Common issues:
# 1. Wrong LIVEKIT_URL format (should include wss://)
# 2. Invalid API credentials
# 3. Network/firewall blocking LiveKit cloud
```

### Agent Not Responding

1. **Verify Gemini API key**: Test at https://aistudio.google.com
2. **Check agent logs**: Look for initialization errors
3. **Try playground**: Use https://agents-playground.livekit.io first
4. **Network test**: Ensure WebRTC connectivity

### LiveAvatar Issues

```bash
# Disable avatar to test audio-only mode
# Remove or comment out in .env:
# LIVEAVATAR_API_KEY=
# AVATAR_ID=
```

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

## 🛠️ Development

### Dependencies

- Python 3.12+
- `livekit-agents[cartesia,deepgram,openai,silero]~=1.3.6`
- `livekit-plugins-google>=1.3.6`
- `livekit-plugins-liveavatar>=1.3.6` (for avatar support)

### Adding Features

The modern architecture makes it easy to extend:

1. **Custom instructions**: Modify `config.agent.instructions` in `config.py`
2. **Different voices**: Change `voice="Puck"` in `agent.py`
3. **Additional modalities**: Add `"VIDEO"` to modalities for multimodal support
4. **Custom VAD**: Replace `voice.VAD.load("silero")` with other options

## 🔄 Migration from Previous Version

If upgrading from the old custom handler implementation:

1. **Backup your .env file**
2. **Run**: `uv sync` to get new dependencies
3. **Update .env**: Change `GEMINI_API_KEY` to `GOOGLE_API_KEY`
4. **Remove old handlers**: Custom handlers are no longer needed
5. **Test**: The agent should work with the same functionality but much simpler code

## 📞 Support

- **LiveKit Documentation**: https://docs.livekit.io/agents/
- **Gemini Live API**: https://ai.google.dev/gemini-api/docs/live
- **LiveAvatar**: https://liveavatar.com
- **Issues**: Report bugs in the project repository

## 🎉 Success!

You now have a modern, production-ready LiveKit Python agent with:
- ✅ Native Gemini Live API integration
- ✅ Real-time Arabic voice conversations
- ✅ Optional visual avatar support
- ✅ Simplified, maintainable codebase
- ✅ Built with 2024 LiveKit best practices
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class LiveKitConfig:
    url: str
    api_key: str
    api_secret: str

@dataclass
class GeminiConfig:
    api_key: str
    model: str = "gemini-2.0-flash-exp"  # Default to working model
    voice: str = "Puck"
    temperature: float = 0.2

@dataclass
class AgentConfig:
    name: str = "Aram Voice Assistant"
    instructions: str = """أنت آرام، مسؤول خدمة الضيوف في فندق مكة المكرمة. تتحدث بالعربية السعودية فقط بأسلوب مهني ومرحب.

مهامك:
- الترحيب بالضيوف وتقديم المساعدة في جميع احتياجاتهم
- تقديم معلومات عن خدمات الفندق (المطاعم، السبا، الصلاة، الواي فاي)
- مساعدة في الحجوزات والاستفسارات
- تقديم نصائح حول مكة المكرمة والمدينة المنورة
- مساعدة في أوقات الصلاة والاتجاهات
- الحفاظ على طابع الضيافة السعودية التقليدية

تحدث بنبرة دافئة ومهنية، واستخدم عبارات الترحيب السعودية المناسبة."""
    room_prefix: str = "call-"

@dataclass
class LiveAvatarConfig:
    api_key: Optional[str] = None
    avatar_id: Optional[str] = None

@dataclass
class Config:
    livekit: LiveKitConfig
    gemini: GeminiConfig
    agent: AgentConfig
    liveavatar: LiveAvatarConfig

def get_config() -> Config:
    """Load configuration from environment variables."""

    # Required environment variables
    livekit_url = os.getenv("LIVEKIT_URL")
    livekit_api_key = os.getenv("LIVEKIT_API_KEY")
    livekit_api_secret = os.getenv("LIVEKIT_API_SECRET")
    google_api_key = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY"))

    if not all([livekit_url, livekit_api_key, livekit_api_secret, google_api_key]):
        raise ValueError("Missing required environment variables. Please check .env file.")

    return Config(
        livekit=LiveKitConfig(
            url=livekit_url,
            api_key=livekit_api_key,
            api_secret=livekit_api_secret
        ),
        gemini=GeminiConfig(
            api_key=google_api_key,
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"),
            voice=os.getenv("GEMINI_VOICE", "Puck"),
            temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.2"))
        ),
        agent=AgentConfig(
            name=os.getenv("AGENT_NAME", "Aram Voice Assistant"),
            room_prefix=os.getenv("ROOM_PREFIX", "call-")
        ),
        liveavatar=LiveAvatarConfig(
            api_key=os.getenv("LIVEAVATAR_API_KEY"),
            avatar_id=os.getenv("AVATAR_ID")
        )
    )
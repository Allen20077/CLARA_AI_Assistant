import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq
from elevenlabs import ElevenLabs


# ============================================================
# CLARA BACKEND
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE, override=True)


# ============================================================
# GET GROQ API KEY
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

print()
print("=" * 60)
print("                 CLARA AI BACKEND")
print("=" * 60)
print("ENV FILE:")
print(ENV_FILE)

if GROQ_API_KEY:
    print("Groq API key: FOUND")
    print("Key starts with:", GROQ_API_KEY[:4])
else:
    print("Groq API key: NOT FOUND")

print("=" * 60)
print()


if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY was not found in backend/.env"
    )

if not ELEVENLABS_API_KEY:
    raise RuntimeError(
        "ELEVENLABS_API_KEY was not found in backend/.env"
    )

# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)
eleven_client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)

# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Clara AI"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    message: str

    language: str = "en-US"


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "assistant": "Clara",
        "message": "Hi! I'm Clara."
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    print()
    print("User:", request.message)
    print("Language:", request.language)

    try:

        languages = {

            "en-US": "English",
            "hi-IN": "Hindi",
            "kn-IN": "Kannada",
            "ta-IN": "Tamil",
            "te-IN": "Telugu",
            "ml-IN": "Malayalam",
            "mr-IN": "Marathi",
            "bn-IN": "Bengali",
            "es-ES": "Spanish",
            "fr-FR": "French",
            "de-DE": "German",
            "ja-JP": "Japanese"

        }

        language_name = languages.get(
            request.language,
            "English"
        )


        system_prompt = f"""
You are Clara.

You are a friendly female AI companion.

Be natural, helpful and conversational.

The user selected {language_name}.

Reply in {language_name}.

Keep normal answers short and useful.

Do not use romantic language.

Do not call the user baby, darling, honey, love, etc.

Do not use excessive emojis.
"""
        response = client.chat.completions.create(

            model="groq/compound",

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": request.message
                }

            ],

            temperature=0.7,

            max_tokens=300

        )


        answer = response.choices[0].message.content


        print("Clara:", answer)


        return {

            "success": True,

            "reply": answer

        }


    except Exception as error:

        print()
        print("=" * 60)
        print("                  GROQ ERROR")
        print("=" * 60)
        print(repr(error))
        print("=" * 60)
        print()


        return {

            "success": False,

            "reply": "Clara's brain is temporarily unavailable."

        }


# ============================================================
# TEXT TO SPEECH
# ============================================================

@app.post("/speak")
def speak(request: ChatRequest):

    try:

        audio = eleven_client.text_to_speech.convert(
            voice_id="YOUR_VOICE_ID",
            model_id="eleven_flash_v2_5",
            text=request.message,
            output_format="mp3_44100_128"
        )

        return StreamingResponse(
            audio,
            media_type="audio/mpeg"
        )

    except Exception as error:

        print("TTS ERROR:", repr(error))

        return {
            "success": False,
            "error": str(error)
        }
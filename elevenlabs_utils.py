from elevenlabs import ElevenLabs

def text_to_speech(text, eleven_api_key, voice_id="default"):
    client = ElevenLabs(api_key=eleven_api_key)
    audio = client.text_to_speech(text=text, voice=voice_id)
    with open("response.mp3", "wb") as f:
        f.write(audio)
    return "response.mp3"

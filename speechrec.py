import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak something...")
    audio = recognizer.listen(source)
    print("Recording complete")

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)

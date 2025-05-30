
import google.generativeai as genai 
import pyttsx3 
import speech_recognition as sr 
import tkinter as tk 
from tkinter import scrolledtext
import threading 
from apikey import api_data


GENAI_API_KEY = api_data

genai.configure(api_key=GENAI_API_KEY)

#Text-to-Speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen_to_command():
    """Speech to Text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        conversation_area.insert(tk.END, "Listening...\n\n")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            query = recognizer.recognize_google(audio, language='en-in').lower()
            conversation_area.insert(tk.END, f"You: {query}\n")
            return query
        except sr.UnknownValueError:
            conversation_area.insert(tk.END, "Friday: Sorry, I didn't catch that. Please repeat.\n")
            speak("Sorry, I didn't catch that. Please repeat.")
            return "none"
        except sr.RequestError:
            conversation_area.insert(tk.END, "Friday: Network error. Please check your connection.\n")
            speak("Network error. Please check your connection.")
            return "none"
        except Exception as e:
            conversation_area.insert(tk.END, f"Friday: Error: {e}\n")
            speak("Sorry, I encountered an error.")
            return "none"


def generate_response(query):
  """Generate a response for the given query using Gemini."""
  try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(query, generation_config = genai.GenerationConfig(
        max_output_tokens=75,
        temperature=0.1,))
    print("\n")
    # response = genai.generate_text(prompt=f"Avinash: {query}\nFriday:")
    return response.text
  except Exception as e:
    return f"Sorry, I encountered an error: {e}"


# Global variable to control the conversation loop
stop_conversation = False


def handle_conversation():
    """Continuously listen to user input and respond."""
    global stop_conversation
    while not stop_conversation:
        query = listen_to_command()
        if query == "none":
            continue

        if "bye" in query or "goodbye" in query:
            conversation_area.insert(tk.END, "Friday: Goodbye! Have a great day!\n")
            speak("Goodbye! Have a great day!")
            break

        # Generate and respond to the user's query
        response = generate_response(query)
        conversation_area.insert(tk.END, f"Friday: {response}\n")
        speak(response)


def start_conversation():
    """Start the conversation"""
    global stop_conversation
    stop_conversation = False
    conversation_thread = threading.Thread(target=handle_conversation)
    conversation_thread.daemon = True
    conversation_thread.start()
    conversation_area.insert(tk.END, "Hi, i am Friday. How can i help you ?\n\n")
    conversation_area.see(tk.END)
    speak("Hi, i am Friday. How can i help you")


def end_conversation():
    """Set the stop_conversation flag to True to end the loop."""
    global stop_conversation
    stop_conversation = True
    conversation_area.insert(tk.END, "Friday: Conversation ended manually. Goodbye!\n")
    speak("Conversation ended manually. Goodbye!")
    root.quit()  # Close the application

# Set up the GUI
# Enhanced GUI setup
root = tk.Tk()
root.title("F-R-I-D-A-Y: Voice Assistant")
root.geometry("700x650")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# Styling constants
TEXT_COLOR = "#ffffff"
BG_COLOR = "#1e1e1e"
ENTRY_BG = "#2e2e2e"
BTN_COLOR = "#3a3a3a"
BTN_HOVER = "#4b4b4b"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 18, "bold")

# Title Label
title_label = tk.Label(
    root, text="F-R-I-D-A-Y (Voice Assistant)", font=TITLE_FONT,
    fg="#00ffd5", bg=BG_COLOR, pady=10
)
title_label.pack()

# Conversation Area
conversation_area = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=70, height=20,
    font=FONT, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR
)
conversation_area.pack(padx=20, pady=15)
conversation_area.config(state='normal')

# Button Frame
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10)

# Custom button style
def style_button(btn):
    btn.configure(
        bg=BTN_COLOR, fg=TEXT_COLOR, font=FONT,
        activebackground=BTN_HOVER, activeforeground="#00ffd5",
        padx=20, pady=10, bd=0, relief=tk.FLAT, cursor="hand2"
    )

# Start Button
start_button = tk.Button(button_frame, text="🎙 Start Conversation", command=start_conversation)
style_button(start_button)
start_button.grid(row=0, column=0, padx=15)

# End Button
end_button = tk.Button(button_frame, text="⛔ End Conversation", command=end_conversation)
style_button(end_button)
end_button.grid(row=0, column=1, padx=15)

root.mainloop()

import speech_recognition as sr
import pyttsx3
from googletrans import Translator
from tkinter import *
from tkinter import messagebox


translator = Translator()
engine = pyttsx3.init()
history = []
def translate_text(event=None):
    try:
        text_to_translate = entry.get()
        translated = translator.translate(text_to_translate, src=source_lang.get(), dest=target_lang.get())
        result_label.config(text=translated.text)
        history.append((text_to_translate, translated.text))
    except Exception as e:
        messagebox.showerror("Error", "Translation Failed! Please check your internet connection.")


def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        result_label.config(text="Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            entry.delete(0, END)
            entry.insert(0, text)
            result_label.config(text="Recognized Speech")
        except sr.UnknownValueError:
            result_label.config(text="Could not understand the audio")
        except sr.RequestError:
            result_label.config(text="Error connecting to the service")
def text_to_speech():
    translated_text = result_label.cget("text")
    if translated_text:
        engine.say(translated_text)
        engine.runAndWait()
    else:
        messagebox.showinfo("Info", "No text to speak. Please translate first.")

def show_history():
    if history:
        history_text = "\n".join([f"{src} -> {tgt}" for src, tgt in history])
        history_window = Toplevel(root)
        history_window.title("Translation History")
        history_window.geometry("400x300")
        history_label = Label(history_window, text=history_text, justify=LEFT, font=("Arial", 10), wraplength=350)
        history_label.pack(pady=10)
    else:
        messagebox.showinfo("Info", "No history available.")

root = Tk()
root.title("Python Translator")
root.geometry("500x450")
root.configure(bg="#f0f0f0")

header_label = Label(root, text="Language Translator", font=("Helvetica", 18, "bold"), bg="#4a90e2", fg="white", pady=10)
header_label.pack(fill=X)

main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack(pady=20)

Label(main_frame, text="Enter text to translate:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
entry = Entry(main_frame, width=40, font=("Arial", 12))
entry.grid(row=0, column=1, padx=10)
entry.bind('<Return>', translate_text)  
source_lang = StringVar(value='en')
target_lang = StringVar(value='es')

Label(main_frame, text="Source (e.g., en):", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky=E)
source_entry = Entry(main_frame, textvariable=source_lang, width=5, font=("Arial", 10))
source_entry.grid(row=1, column=1, padx=10, sticky=W)

Label(main_frame, text="Target (e.g., es):", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky=E)
target_entry = Entry(main_frame, textvariable=target_lang, width=5, font=("Arial", 10))
target_entry.grid(row=2, column=1, padx=10, sticky=W)

Button(main_frame, text="Translate", command=translate_text, font=("Arial", 12), bg="#4CAF50", fg="white", width=10).grid(row=3, column=1, padx=10, pady=10, sticky=W)
result_label = Label(main_frame, text="", font=("Arial", 14), wraplength=350, justify=LEFT, bg="#f0f0f0")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

Button(main_frame, text="Voice Input", command=voice_to_text, font=("Arial", 12), bg="#4a90e2", fg="white", width=10).grid(row=5, column=0, padx=10, pady=10)
Button(main_frame, text="Speak", command=text_to_speech, font=("Arial", 12), bg="#FF5722", fg="white", width=10).grid(row=5, column=1, padx=10, pady=10, sticky=W)
Button(main_frame, text="Show History", command=show_history, font=("Arial", 12), bg="#607D8B", fg="white", width=10).grid(row=6, column=1, padx=10, pady=10, sticky=W)

root.mainloop()

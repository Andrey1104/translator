import tkinter as tk
from deep_translator import GoogleTranslator
import speech_recognition as sr

def recognize_and_translate_speech(recognizer, microphone, dest_language="cs"):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        status_label.config(text="Говорите...")
        audio = recognizer.listen(source, phrase_time_limit=None)

    audio_response = {
        "success": True,
        "error": None,
        "transcription": None,
        "translation": None
    }

    try:
        audio_response["transcription"] = recognizer.recognize_google(audio, language="uk")

        translated = GoogleTranslator(source='uk', target=dest_language).translate(audio_response["transcription"])
        audio_response["translation"] = translated

    except sr.RequestError:
        audio_response["success"] = False
        audio_response["error"] = "API unavailable"
    except sr.UnknownValueError:
        audio_response["error"] = "Unable to recognize speech"
    except Exception as e:
        audio_response["success"] = False
        audio_response["error"] = str(e)

    return audio_response

def on_translate_button_click():
    response = recognize_and_translate_speech(recognizer, microphone, dest_language="cs")
    if response["transcription"]:
        transcription_label.config(text="Ваше сообщение: " + response["transcription"])
        translation_label.config(text="Перевод: " + response["translation"])
    if not response["success"]:
        status_label.config(text="Ошибка: " + response["error"])
    if response["error"]:
        status_label.config(text="Пожалуйста, попробуйте еще раз")

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    root = tk.Tk()
    root.title("Распознавание и перевод речи")

    transcription_label = tk.Label(root, text="Ваше сообщение: ")
    transcription_label.pack()

    translation_label = tk.Label(root, text="Перевод: ")
    translation_label.pack()

    translate_button = tk.Button(root, text="Перевести", command=on_translate_button_click)
    translate_button.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    root.mainloop()

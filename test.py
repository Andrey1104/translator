import time
import pyttsx3
import speech_recognition as sr
from deep_translator import GoogleTranslator

INPUT_LANG = "cs"
OUTPUT_LANG = "en"
LANG = ["en", "de", "cs"]


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result
    return wrapper


@timer
def recognize_and_translate_speech(s_recognizer, my_microphone):
    if not isinstance(s_recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(my_microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with my_microphone as source:
        s_recognizer.adjust_for_ambient_noise(source)
        print("Start to speak:")
        audio = s_recognizer.listen(source, phrase_time_limit=None)
        
    audio_response = {
        "success": True,
        "error": None,
        "transcription": None,
        "translation": None
    }

    try:
        audio_response["transcription"] = s_recognizer.recognize_google(audio, language=INPUT_LANG)
        translation = GoogleTranslator(source=INPUT_LANG, target=OUTPUT_LANG).translate(audio_response["transcription"])

        # translations = [GoogleTranslator(source="uk", target=language).translate(audio_response["transcription"]) for language in LANG]
        # audio_response["translation_cs"] = translations[-1]
        # audio_response["translation_de"] = translations[1]
        # audio_response["translation_en"] = translations[0]

        audio_response["translation"] = translation

    except sr.RequestError:
        audio_response["success"] = False
        audio_response["error"] = "API unavailable"
    except sr.UnknownValueError:
        audio_response["error"] = "Unable to recognize speech"
    except Exception as e:
        audio_response["success"] = False
        audio_response["error"] = str(e)

    return audio_response


@timer
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 250)
    engine.setProperty('volume', 0.9)

    engine.say(text)
    engine.runAndWait()


@timer
def get_microphone():
    try:
        return sr.Microphone()
    except OSError:
        print("No default input device available. Retrying in 5 seconds...")
        return None


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = get_microphone()

    while microphone is None:
        time.sleep(5)
        microphone = get_microphone()

    try:
        while True:
            response = recognize_and_translate_speech(recognizer, microphone)

            if response["transcription"]:
                print("----------------------------------------------------------------------")
                print(f"Speaker: {response['transcription']}")
                # print(f"\nEnglish : {response['translation_en']}")
                # print(f"\nGerman : {response['translation_de']}")
                # print(f"\nCzech : {response['translation_cs']}")
                print(f"\nEnglish : {response['translation']}")
                print("----------------------------------------------------------------------")
                # speak(response['translation'])

            if not response["success"]:
                print("Error: {}".format(response["error"]))
            if response["error"]:
                print(response["error"])
                print("Repeat, please")
    except KeyboardInterrupt:
        print("Application is shutting down...")

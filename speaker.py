import speech_recognition as sr

from test import timer

INPUT_LANG = "cs"
OUTPUT_LANG = "uk"
LANG = ["en", "de", "cs"]


@timer
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.listen(source, phrase_time_limit=None)

            try:
                text = recognizer.recognize_google(audio, language=INPUT_LANG)
                print(f"You said: {text}.")

                with open("speech.txt", "a+", encoding="utf-8") as file:
                    file.write(text + "\n")

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    except Exception as err:
        print(f"Could not access the microphone; {err}")

    return None


if __name__ == "__main__":
    try:
        while True:
            recognize_speech_from_mic()
    except KeyboardInterrupt:
        print("Application is shutting down...")
    except Exception as error:
        print(f"Error: {error}")

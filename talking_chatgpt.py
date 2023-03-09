'''---------------------------------Library section----------------------------'''

# Import the OpenAI library
import openai

# Import summarizer library
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
# nltk.download('punkt')

# import library for voice creation
import pyttsx3

# import library for voice recognition
import speech_recognition as sr

# import translation library
from googletrans import Translator

'''----------------------------------api and model---------------------------'''

# Set up the OpenAI API client :
openai.api_key = "your api"

# Set up the model (more models, visit https://beta.openai.com/playground)
model_engine = "text-davinci-003"


'''---------------------------------book of functions--------------------------'''

# Define a function that sends a message to ChatGPT
def chat_query(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

# Define a function that handles the conversation
def conversation_handler(prompt):
    # Send the prompt to ChatGPT
    response = chat_query(prompt)
    return response

### Creating function to summarize long sentence
def summarize(text, n=3):
    # tokenize the text into sentences
    sentences = sent_tokenize(text)

    # remove stopwords and stem the words
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()
    words = [word_tokenize(sentence) for sentence in sentences]
    words = [[ps.stem(word.lower()) for word in sentence if word.lower() not in stop_words] for sentence in words]

    # calculate the word frequency
    frequency = {}
    for sentence in words:
        for word in sentence:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1

    # sort the sentences by score
    score = {}
    for i in range(len(sentences)):
        for word in words[i]:
            if word in frequency:
                if i in score:
                    score[i] += frequency[word]
                else:
                    score[i] = frequency[word]

    top_sentences = sorted(score, key=score.get, reverse=True)[:n]
    summary = [sentences[i] for i in top_sentences]
    return " ".join(summary)

### Creating function that converts text-to-speech
def speak(text):
    # initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # set the speech rate and volume
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    engine.setProperty('voice', voice_id)

    # convert the text to speech
    engine.say(text)
    engine.runAndWait()

# Creating take command function
def takeCommand():
    #It takes microphone input from the user and returns string output
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source, timeout=5)
    # Note: It might also recieve background sound and can create error. So, to avoid this, we need to apply try and error.
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:
        print(e)    
        print("Sorry I didn't understand...")   #Say that again will be printed in case of improper voice 
        speak("Sorry I didn't understand...")
        return "None" #None string will be returned
    return query

'''-----------------------------main program starts here-------------------------'''

### getting voice input
# create a recognizer object
r = sr.Recognizer()

# chat gpt working
if __name__ == "__main__":
  # Start the conversation
  speak("Hello! I am your personal assistant. What do you want to know?")
  query3 = 'yes'
  while(True):
      if 'yes' in query3:
        speak('Ask your question')
        query1 = takeCommand().lower()
        speak('Please choose: summary or description')
        query2 = takeCommand().lower()      
      
        print('Processing your task. Please wait....')  
        if 'summary' in query2:
            sen = conversation_handler(query1)
            summary = summarize(sen,n=2)
            speak('Whether you want written summary or verbal summary')
            query4 = takeCommand().lower()
            if 'written' in query4:
                speak('Here is your written summary')
                print(summary)
            else:
                print(summary)
                speak(summary)
        else:
            sen = conversation_handler(query1)
            speak('Do you want written description or verbal description?')
            query5 = takeCommand().lower()
            if 'written' in query5:
                speak('Here is your written description')
                print(sen)
            else:
                print(sen)
                speak(sen)
        
        speak('Would you like to continue?')
        query3 = takeCommand().lower()
              
      elif 'no' in query3:
        print('Thank you for your questions. Have a nice day.')
        speak('Thank you for your questions. Have a nice day.')
        break    
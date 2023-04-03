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

# import google news libraries
from GoogleNews import GoogleNews as GN
import pandas as pd

# for image generation
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from PIL import Image
'''----------------------------------api and model---------------------------'''

# Set up the OpenAI API client :
openai.api_key = "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"

# Set up the model (more models, visit https://beta.openai.com/playground)
model_engine = "text-davinci-003"


'''---------------------------------book of functions--------------------------'''

# creating chatGPT class
class chatGPT:
    # Define a function that sends a message to ChatGPT
    def chat_query(self, prompt):
        completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=512,
        n=1,
        temperature=0.5,
        )

        message = completions.choices[0].text
        return message

    # Define a function that handles the conversation
    def conversation_handler(self, prompt):
        # Send the prompt to ChatGPT
        response = self.chat_query(prompt)
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

# function to get temperature of a location
def getTemperture(location):
    import requests
    from bs4 import BeautifulSoup   
    # Enter the City Name
    search = "Temperture in {}".format(location)
 
    # URL
    url = f"https://www.google.com/search?&q={search}"
  
    # Sending HTTP request
    req = requests.get(url)
 
    # Pulling HTTP data from internet
    sor = BeautifulSoup(req.text, "html.parser")
          
    # Getting the required data
    data = sor.find("div", class_='BNeawe').text
    print(f'The temperature in {location} is {data}')
    speak(f'The temperature in {location} is {data}')


# ------
# function to get google news
def getNews(location):
    news = GN(period='1d')
    news.search(location)
    result = news.result()
    data = pd.DataFrame.from_dict(result)
    return data


# generate image
def gen_image(query):
    # Set the directory where you want to save the images
    directory = "images"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Search for images
    url = f"https://www.google.com/search?q={query}&tbm=isch&tbs=ic:specific,isc:white,isz:lt,islt:qsvga"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_tags = soup.find_all("img")

    # Download the images to the local directory
    for i, image in enumerate(image_tags[3:4]):
        url = image["src"]
        if not url.startswith("http"):
            url = f"https://www.google.com{url}"
        filename = f"{query.replace(' ', '_')}_{i}.jpg"
        filepath = os.path.join(directory, filename)
        urllib.request.urlretrieve(url, filepath)
        # Open the downloaded image file
        img = Image.open(filepath)
        # Show the image
        img.show()


'''-----------------------------main program starts here-------------------------'''

### getting voice input
# create a recognizer object
r = sr.Recognizer()

# chat gpt working
if __name__ == "__main__":
  # Start the conversation
  speak("Hello! I am your personal assistant. How can i help you?")
  query6 = takeCommand().lower()
  if '' in query6:
      speak('Here is a list of task available')
      speak('Current affairs such as news, temperature, download images or any explanation from Chat GPT')
  else:
      speak('Here is a list of task available')
      speak('Current affairs such as news, temperature, image download or any explanation from Chat GPT')

  query7 = takeCommand().lower()
  while(True):
      if ('news' in query7):
          speak('Please tell me the location: city, state or country')
          location = takeCommand().lower()
          news = getNews(location)
          speak("Do you want to listen to the news or wanna read only?")
          query9 = takeCommand().lower()
          if 'listen' in query9:
              speak(f"Here are the today's top 5 news of{location}")
              x = 1
              for elem in news['title']:
                  print(elem)
                  speak(f'News number {x}:')
                  speak(elem)
                  x+=1
                  if x==6:
                      break
          else:
              speak(f"Here are the today's top 5 news of{location}")
              print(news)
          speak('Do you want to know news of some other places. If not, you can choose temperature, image download or connect to chat gpt, or do nothing')
          query7 = takeCommand().lower()
          if 'nothing' in query7:
              print('Thank you for your questions. Have a nice day')
              speak('Thank you for your questions. Have a nice day')
              break

      if ('temperature' in query7):
          speak('please tell me the location: city, state or country')
          query8 = takeCommand().lower()
          temp = getTemperture(query8)
          print(temp)
          speak('Do you want to know temperature of some other place. If not, you can choose news, image download or connect to chat gpt, or do nothing')
          query7 = takeCommand().lower()
          if 'nothing' in query7:
              print('Thank you for your questions. Have a nice day')
              speak('Thank you for your questions. Have a nice day')
              break
          
      if ('download' in query7):
          speak('please tell me which image you want to download')
          query10 = takeCommand().lower()
          img1 = gen_image(query10)
          print(img1)
          speak('Do you want to download some more image. If not, you can choose news, temperature or connect to chat gpt, or do nothing')
          query7 = takeCommand().lower()
          if 'nothing' in query7:
              print('Thank you for your questions. Have a nice day')
              speak('Thank you for your questions. Have a nice day')
              break
          
      if ('chat gpt' in query7):
            #   ------
            query3 = 'yes'
            while(True):
                if 'yes' in query3:
                    speak('Ask your question')
                    query1 = takeCommand().lower()
                    speak('Please choose: summary or description')
                    query2 = takeCommand().lower()      
                    # creating an instance for chatGPT class named talkGPT
                    talkGPT = chatGPT()
                    print('Processing your task. Please wait....')  
                    if 'summary' in query2:
                        sen = talkGPT.conversation_handler(query1)
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
                        sen = talkGPT.conversation_handler(query1)
                        speak('Do you want written description or verbal description?')
                        query5 = takeCommand().lower()
                        if 'written' in query5:
                            speak('Here is your written description')
                            print(sen)
                        else:
                            print(sen)
                            speak(sen)
        
                    speak('Would you like to continue with chat GPT?')
                    query3 = takeCommand().lower()
              
                elif 'no' in query3:
                    break    
                    #   ------  
            speak('what else i can do: temperature or news or nothing')
            query7 = takeCommand().lower()
            if 'nothing' in query7:
                print('Thank you for your questions. Have a nice day')
                speak('Thank you for your questions. Have a nice day')
                break

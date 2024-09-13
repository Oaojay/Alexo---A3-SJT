import getpass
import os
import speech_recognition as sr
import pyttsx3
import pyaudio
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

# Carregar o DataFrame
df = pd.read_csv("idoso.csv")

# Definir chave de API diretamente no código
os.environ["GOOGLE_API_KEY"] = getpass.getpass =("AIzaSyC0xY0MSy2XZ0zoxdBHuY5unfEYF7humWU")

# Configuração do modelo de linguagem
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2)

# Prompt para o agente
agent_prompt_prefix = """   
Você se chama alexo, e está trabalhando com um dataframe pandas no python.
O nome do Dataframe é `df`.
"""

# Criar o agente
agent = create_pandas_dataframe_agent(
    llm,
    df,
    prefix=agent_prompt_prefix,
    verbose=True,
    allow_dangerous_code=True
)

# Configuração da síntese de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Velocidade da fala
engine.setProperty('volume', 1)  # Volume (0.0 a 1.0)

# Função para falar texto
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Função para capturar a entrada de voz
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Estou ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Reconhecendo...")
        query = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {query}")
        return query
    except sr.UnknownValueError:
        speak("Desculpe, não entendi o que você disse.")
        return None
    except sr.RequestError:
        speak("Erro ao se conectar ao serviço de reconhecimento de voz.")
        return None

# Loop principal do assistente de voz
while True:
    speak("Como posso ajudar você?")
    user_input = listen()
    if user_input:
        # Passar o comando do usuário para o agente
        response = agent.run(user_input)
        print(response)
        speak(response)
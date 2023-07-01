import os
import csv
import api
from dotenv import load_dotenv
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from pymongo import MongoClient

data_path = os.path.join(os.path.dirname(__file__), "training_data", "general.csv")

load_dotenv(dotenv_path="/Users/reneemundie/PythonProjects/api-chatbot/.venv/mongo_uri.env")
mongo_uri = os.getenv('mongo_uri')

MONGO_URI = mongo_uri
client = MongoClient(MONGO_URI)
database_name = "chat_logs"
collection_name = "chat"
database = client[database_name]
collection = database[collection_name]

chatbot = ChatBot(
    'MyBot',
    read_only=True,
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database=database,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
     logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ],
)

corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")

list_trainer = ListTrainer(chatbot)
with open(data_path, 'r', encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        list_trainer.train([row[0], row[1]])

chat_data = {
    'conversation': []
}

def start_chat(payload):
    py_list = api.py_weather_data()
    user_input = payload['message']
    user_input_statement = Statement(text=user_input)

    if "bye" in user_input.lower():
        bot_response = "Goodbye!"

    elif "weather" in user_input.lower():
        location = None
        for data in py_list:
            if "Location" in data:
                if data["Location"].lower() in user_input.lower():
                    location = data
                    break
        if location is not None:
            temperature = location.get("Temperature")
            description = location.get("Description")
            feels_like = location.get("Feels Like")
            bot_response = f"Temperature: {temperature}\nFeels Like: {feels_like}\nDescription: {description}"
        
        else:
            bot_response = "Sorry, I can't find the weather data for that location."

    else:
        bot_response = chatbot.get_response(user_input_statement)

    chat_data['conversation'].append({
        'bot_response': str(bot_response),
        'user_input': user_input
    })

    if collection.count_documents({}) == 0:
        collection.insert_one(chat_data)
    else:
        collection.replace_one({}, chat_data)

    return str(bot_response)
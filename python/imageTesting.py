import unitest
from dotenv import load_dotenv
from sightengine import Client
from PIL import Image
import os


load_dotenv()

api_key = os.getenv('SIGHT_ENGINE_API_USER')
api_secret = os.getenv('SIGHT_ENGINE_API_SECRET')

client = Client(api_key, api_secret)
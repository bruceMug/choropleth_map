from os import environ
from dotenv import load_dotenv
load_dotenv()

DATABASE = environ.get('DATABASE')
USER = environ.get('USER')
PASSWORD = environ.get('PASSWORD')
HOST = environ.get('HOST')
PORT = environ.get('PORT')


# // function that returns random values in a space

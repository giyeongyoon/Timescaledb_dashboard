import os
from dotenv import load_dotenv


load_dotenv()

conf = {
    "email": os.getenv("email"),
    "password": os.getenv("password"),
    "secret_key": os.getenv("secret_key"),
    "email_pw": os.getenv("email_pw")
}
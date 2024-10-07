from waitress import serve
from dotenv import load_dotenv

load_dotenv(verbose=True)

from app import app

serve(app, host="0.0.0.0", port=7890)

from app import mongo, create_app
from app.usermodel import User
from app.tracker import Tracker

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'mongo': mongo, 'User': User}
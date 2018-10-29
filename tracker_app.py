from app import mongo, create_app
from app.usermodel import User
from app.tracker import Tracker
from app.projectmodel import TrkProject
from flask import session
from flask_login import login_required

app = create_app()

@app.context_processor
def add_session_project_processor():
    project_choices=[('ALL','')]
    project_choices+=( [(p.id,p.name) for p in TrkProject.get_all()])
    val=''
    print(project_choices)
    if 'sessionproject' in session:
        val=session['sessionproject']
    return {'project_choices':project_choices, 'sessionproject':val}

@login_required
@app.route('/set_session_project/<id>', methods=['POST'])
def set_session_project(id):
    session['sessionproject']=id
    return ''

@app.shell_context_processor
def make_shell_context():
    return {'mongo': mongo, 'User': User}

from app.projects import bp
from flask import url_for, request, render_template, current_app, flash,redirect, jsonify
from flask_login import login_required, current_user
from app.projects.forms import AddEditProjectForm
from app.projectmodel import TrkProject
import os



@bp.route('/projectlist')
@login_required
def projectlist():
    page = request.args.get('page', 1, type=int)
    projects = TrkProject.get_list_projects(page, int(current_app.config['PROJECTS_PER_PAGE']))
    prev_url = url_for('projects.projectlist', page=projects.prev) if projects.has_prev else None
    next_url = url_for('projects.projectlist', page=projects.next) if projects.has_next else None
    return render_template('projects/projectlist.html', title='projects',
                       prev_url=prev_url, next_url=next_url, projects=projects.projects )



@bp.route('/project_info/<id>', methods=['GET', 'POST'])
@login_required
def project_info(id):
    
    project = TrkProject.get_project(id)
    
    if project is None:
        flash('project with id {} does not exist'.format(id))
        return redirect(url_for('projects.projectlist'))
    if request.method == 'POST':
        if request.form['action'] == 'edit':
            return redirect(url_for('projects.project_edit', id=project.id))
        elif request.form['action'] == 'back': 
            return redirect(url_for('projects.projectlist'))
        else:
            flash('Something strange happened here')
            return redirect(url_for('projects.projectlist'))
    else:
        return render_template('projects/project_info.html', project=project, title=project.name)


@bp.route('/project_edit/<id>', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    project = TrkProject.get_project(id)
    
    if project is None:
        flash('project with id {} does not exist'.format(id))
        return redirect(url_for('projects.projectlist'))
    form = AddEditProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.update_project()
        flash('Project  {} updated'.format(project.name))
        return redirect(url_for('projects.projectlist'))
    else:
        return render_template('projects/project_edit.html', form=form,project=project, title=project.name)


@bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = AddEditProjectForm()
    if form.validate_on_submit():
        project=TrkProject.create_project(form.name.data, form.description.data)
        return redirect(url_for('projects.project_info', id= project.id))
    return render_template('projects/add_project.html', form=form, title='Add project')




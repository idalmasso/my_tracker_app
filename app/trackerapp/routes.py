from app.trackerapp import bp
from flask import url_for, request, render_template, send_from_directory, current_app, flash, redirect, session
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.trackerapp.forms import AddTrackerForm, EditTrackerForm
from app.tracker import Tracker
from app.projectmodel import TrkProject
from app.usermodel import User
from app.trackerchangesmodel import TrkChanges
import os
from .lookup import *


@bp.route('/')
@login_required
def index():
    filt = {}
    if 'sessionproject' in session:
        if session['sessionproject'] != 'ALL':
            filt = {'project': session['sessionproject']}
    page = request.args.get('page', 1, type=int)
    changes = TrkChanges.get_list_changes(page, int(current_app.config['TRACKER_PER_PAGE']), filt)
    prev_url = url_for('trackerapp.index', page=changes.prev) if changes.has_prev else None
    next_url = url_for('trackerapp.index', page=changes.next) if changes.has_next else None
    return render_template('trackerapp/listchanges.html', title='Last changes',
                           prev_url=prev_url, next_url=next_url, changes=changes.changes)


@bp.route('/trackerlist/<filter_tracker>')
@login_required
def trackerlist(filter_tracker):
    filtering = {}
    if 'sessionproject' in session:
        if session['sessionproject'] != 'ALL':
            filtering = {'project': session['sessionproject']}
    if filter_tracker == 'open':
        filtering.update({'status': {'$in': [0, 1]}})
    if filter_tracker == 'closed':
        filtering.update({'status': {'$nin': [0, 1]}})
    page = request.args.get('page', 1, type=int)
    trackers = Tracker.get_list_trackers(page, int(current_app.config['TRACKER_PER_PAGE']), filtering=filtering)
    prev_url = url_for('trackerapp.trackerlist', filter_tracker=filter_tracker, page=trackers.prev) \
        if trackers.has_prev else None
    next_url = url_for('trackerapp.trackerlist', filter_tracker=filter_tracker, page=trackers.next) \
        if trackers.has_next else None
    return render_template('trackerapp/trackerlist.html', title='Trackers',
                           prev_url=prev_url, next_url=next_url, trackers=trackers.trackers, statuses=dict(STATUSES),
                           priorities=dict(PRIORITIES), categories=dict(CATEGORIES))


@bp.route('/tracker/<id>')
@login_required
def tracker(id):
    tracker = Tracker.get_tracker(id)
    return render_template('trackerapp/tracker.html', tracker=tracker, title=Tracker.title)


@bp.route('/tracker/<id>/popup')
@login_required
def tracker_popup(id):
    tracker = Tracker.get_tracker(id)
    if tracker is not None:
        return render_template('trackerapp/tracker_popup.html', tracker=tracker)
    return redirect(url_for('trackerapp.trackerlist', filter_tracker='open'))


@bp.route('/tracker_info/<id>', methods=['GET', 'POST'])
@login_required
def tracker_info(id):
    tracker = Tracker.get_tracker(id)
    if tracker is None:
        flash('tracker with id {} does not exist'.format(id))
        return redirect(url_for('trackerapp.trackerlist', filter_tracker='open'))
    if request.method == 'POST':
        if request.form['action'] == 'edit':
            return redirect(url_for('trackerapp.tracker_edit', id=tracker.id))
        elif request.form['action'] == 'back':
            return redirect(url_for('trackerapp.trackerlist', filter_tracker='open'))
        else:
            flash('Something strange happened here')
            return redirect(url_for('trackerapp.trackerlist'))
    else:
        return render_template('trackerapp/tracker_info.html', tracker=tracker, title=Tracker.title,
                               statuses=dict(STATUSES), priorities=dict(PRIORITIES), categories=dict(CATEGORIES))


@bp.route('/tracker_edit/<id>', methods=['GET', 'POST'])
@login_required
def tracker_edit(id):
    tracker = Tracker.get_tracker(id)
    if tracker is None:
        flash('tracker with id {} does not exist'.format(id))
        return redirect(url_for('trackerapp.trackerlist', filter_tracker='open'))
    form = EditTrackerForm(obj=tracker)
    form.project.choices = [(p.id, p.name) for p in TrkProject.get_all()]
    form.user_assigned.choices = [(u.username, u.username) for u in User.get_list_enabled_users()]
    if not form.project.choices:
        flash('No Projects exist!')
        return redirect(url_for('projects.projectlist'))
    if form.validate_on_submit():
        tracker.title = form.title.data
        tracker.description = form.description.data
        tracker.priority = int(form.priority.data)
        tracker.status = int(form.status.data)
        tracker.project = form.project.data
        tracker.user_assigned = form.user_assigned.data
        tracker.prefix = TrkProject.get_project(tracker.project).prefix
        tracker.categories = form.categories.data
        files = form.images.data
        action = 'EDITED'
        for f in files:
            if f is not None and not f == '':
                filename = secure_filename(f.filename)
                if allowed_file(filename):
                    if filename not in tracker.filenames:
                        tracker.filenames.append(filename)
                    if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], tracker.id)):
                        os.mkdir(os.path.join(current_app.config['UPLOAD_FOLDER'], tracker.id))
                    f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], tracker.id,
                                        filename))
                    action = 'ADDED IMAGES'
                    tracker.user_assigned = current_user.username
                    if tracker.status == 0:
                        tracker.status = 1  #working
                else:
                    flash('File {} skipped because not image'.format(filename))
        tracker.update_tracker_by_form()
        flash('Tracker  {} updated'.format(tracker.number))
        TrkChanges.create_change(current_user.username, tracker, tracker.project, action)
        return redirect(url_for('trackerapp.trackerlist', filter_tracker='open'))
    else:
        return render_template('trackerapp/tracker_edit.html', form=form, tracker=tracker, title=Tracker.title)


@bp.route('/add_tracker', methods=['GET', 'POST'])
@login_required
def add_tracker():
    form = AddTrackerForm()
    form.project.choices = [(p.id, p.name) for p in TrkProject.get_all()]
    form.user_assigned.choices = [(u.username, u.username) for u in User.get_list_enabled_users()]
    form.user_assigned.data = current_user.username
    if 'sessionproject' in session and session['sessionproject'] != 'ALL':
        form.project.data = session['sessionproject']
    if not form.project.choices:
        flash('No Projects exist!')
        return redirect(url_for('projects.projectlist', filter_tracker='open'))
    if form.validate_on_submit():
        tracker = Tracker.add_tracker(form.title.data, form.project.data)
        tracker.description = form.description.data
        tracker.priority = int(form.priority.data)
        tracker.project = form.project.data
        tracker.prefix = TrkProject.get_project(tracker.project).prefix
        tracker.categories = form.categories.data
        tracker.user_assigned = form.user_assigned.data
        files = form.images.data

        for f in files:
            if f is not None and not f == '':
                filename = secure_filename(f.filename)
                if allowed_file(filename):
                    tracker.filenames.append(filename)
                    if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], tracker.id)):
                        os.mkdir(os.path.join(current_app.config['UPLOAD_FOLDER'], tracker.id))
                    f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], tracker.id,
                                        filename))
                else:
                    flash('File {} skipped because not image'.format(filename))
        tracker.update_tracker_by_form()
        TrkChanges.create_change(current_user.username, tracker, tracker.project, 'CREATED')
        return redirect(url_for('trackerapp.tracker_info', id=tracker.id))
    return render_template('trackerapp/add_tracker.html', form=form, title='Add tracker')


@bp.route('/delete_tracker/<id>', methods=['POST'])
@login_required
def delete_tracker(id):
    if current_user.admin:
        Tracker.get_tracker(id).remove_tracker()
        TrkChanges.create_change(current_user.username, tracker, tracker.project, 'DELETED')
    return redirect(url_for('trackerapp.trackerlist', filter_tracker='open'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/uploads/<tracker_id>/<filename>')
def uploaded_file(tracker_id, filename):
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], tracker_id),
                               filename)

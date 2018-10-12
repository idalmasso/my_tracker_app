from app.trackerapp import bp
from flask import url_for, request, render_template, send_from_directory, current_app, flash,redirect, jsonify
from flask_login import login_required, current_user
from app.trackerapp.forms import AddTrackerForm
from app.tracker import Tracker
import os



@bp.route('/')
def index():
    return render_template('index.html', title='Home')


@bp.route('/trackerlist')
@login_required
def trackerlist():
    page = request.args.get('page', 1, type=int)
    trackers = Tracker.get_list_trackers(page, int(current_app.config['TRACKER_PER_PAGE']))
    prev_url = url_for('trackerapp.trackerlist', page=trackers.prev) if trackers.has_prev else None
    next_url = url_for('trackerapp.trackerlist', page=trackers.next) if trackers.has_next else None
    return render_template('trackerapp/trackerlist.html', title='trackers',
                           prev_url=prev_url, next_url=next_url, trackers=trackers.trackers)


@bp.route('/tracker/<id>')
@login_required
def tracker(id):
    tracker = Tracker.get_tracker(id)
    if Tracker.torrent_status == 'completed':
        filename = url_for('trackerapp.send_file', id=Tracker.id)
        return render_template('trackerapp/tracker.html', tracker=tracker, title=Tracker.title, filename=filename)
    return redirect(url_for('trackerapp.trackerlist'))


@bp.route('/tracker/<id>/popup')
@login_required
def tracker_popup(id):
    tracker = Tracker.get_tracker(id)
    if tracker is not None:
        return render_template('trackerapp/tracker_popup.html', tracker=tracker)
    return redirect(url_for('trackerapp.trackerlist'))

	
@bp.route('/tracker_info/<id>', methods=['GET', 'POST'])
@login_required
def tracker_info(id):
    tracker = Tracker.get_tracker(id)
    
    if tracker is None:
        flash('tracker with id {} does not exist'.format(id))
        return redirect(url_for('trackerapp.trackerlist'))
    if request.method == 'POST':
        return redirect(url_for('trackerapp.trackerlist'))
    else:
        return render_template('trackerapp/tracker_info.html', tracker=tracker, title=Tracker.title)

		
@bp.route('/add_tracker', methods=['GET', 'POST'])
@login_required
def add_tracker():
    form = AddTrackerForm()
    if form.validate_on_submit():
        Tracker.add_tracker(form.title.data)
        return redirect(url_for('trackerapp.trackerlist'))
    return render_template('trackerapp/add_tracker.html', form=form, title='Add tracker')


@bp.route('/delete_tracker/<id>', methods=['POST'])
@login_required
def delete_tracker(id):
    if current_user.admin:
        Tracker.get_tracker(id).remove_tracker()
    return redirect(url_for('trackerapp.trackerlist'))


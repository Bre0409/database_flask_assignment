from flask import Blueprint, render_template, request, redirect, url_for

# Views blueprint created
views = Blueprint('views', __name__)  

# Day options
DAY_NAMES = ["Today", "Tomorrow", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@views.route('/tasks', methods=['GET', 'POST'])
def task_list():
    selected_day = request.args.get('day', 'Today')
    if selected_day not in DAY_NAMES:
        selected_day = 'Today'

    if request.method == 'POST':
        # No saving, just redirect back
        return redirect(url_for('views.task_list', day=selected_day))

    return render_template(
        'daily_organiser.html',
        tasks=[],
        selected_day=selected_day,
        selected_day_index=DAY_NAMES.index(selected_day)
    )

@views.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    return redirect(request.referrer or url_for('views.task_list'))

@views.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    return redirect(request.referrer or url_for('views.task_list'))

@views.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    return redirect(request.referrer or url_for('views.task_list'))

@views.route('/')
def index():
    return redirect(url_for('auth.home'))

@views.route('/calendar')
def calendar():
    return render_template('calendar.html', events=[])

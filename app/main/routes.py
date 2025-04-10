from flask import render_template, redirect, url_for, request, flash, session
from app import db
from app.models import User, WeightEntry, WeightGoal, BMIEntry
from datetime import datetime, date
from app.utils import convert_weight, calculate_bmi, bmi_category, calculate_weekly_target
import plotly.graph_objs as go
import json
from plotly.utils import PlotlyJSONEncoder

from app.main import bp


def login_required(func):
    """
    Decorator to enforce login.
    """
    from functools import wraps
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return decorated_function


@bp.route('/')
@login_required
def dashboard():
    """
    Dashboard displaying current weight, BMI, goal progress, and a weight trend chart.
    """
    user = User.query.get(session['user_id'])
    weight_entries = WeightEntry.query.filter_by(user_id=user.id).order_by(WeightEntry.date).all()
    goal = WeightGoal.query.filter_by(user_id=user.id).first()
    bmi_entries = BMIEntry.query.filter_by(user_id=user.id).order_by(BMIEntry.date).all()

    latest_weight = weight_entries[-1] if weight_entries else None
    bmi_value = None
    bmi_cat = None
    if latest_weight and user.height:
        bmi_value = calculate_bmi(latest_weight.weight_kg, user.height)
        bmi_cat = bmi_category(bmi_value)
        # Record the BMI entry.
        bmi_record = BMIEntry(user_id=user.id, bmi_value=bmi_value, category=bmi_cat, date=datetime.utcnow())
        db.session.add(bmi_record)
        db.session.commit()

    # Prepare Plotly line chart for weight entries.
    dates = [we.date.strftime('%Y-%m-%d') for we in weight_entries]
    display_unit = 'lbs' if user.unit_preference == 'imperial' else 'kg'
    weights = [convert_weight(we.weight_kg, 'kg', display_unit) for we in weight_entries]
    goal_line = []
    if goal:
        goal_line = [convert_weight(goal.goal_weight_kg, 'kg', display_unit)] * len(dates)

    trace_actual = go.Scatter(x=dates, y=weights, mode='lines+markers', name='Weight')
    data = [trace_actual]
    if goal_line:
        trace_goal = go.Scatter(x=dates, y=goal_line, mode='lines', name='Goal Weight', line=dict(dash='dash'))
        data.append(trace_goal)
    layout = go.Layout(
        title='Weight Trend',
        xaxis={'title': 'Date'},
        yaxis={'title': f'Weight ({display_unit})'}
    )
    graphJSON = json.dumps({'data': data, 'layout': layout}, cls=PlotlyJSONEncoder)

    weekly_target = None
    if latest_weight and goal:
        weekly_target = calculate_weekly_target(latest_weight.weight_kg, goal.goal_weight_kg, date.today(),
                                                goal.target_date)

    return render_template('main/dashboard.html',
                           user=user,
                           latest_weight=latest_weight,
                           bmi_value=bmi_value,
                           bmi_cat=bmi_cat,
                           graphJSON=graphJSON,
                           weekly_target=weekly_target,
                           goal=goal)


@bp.route('/add_weight', methods=['GET', 'POST'])
@login_required
def add_weight():
    """
    Record a new weight entry.
    """
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        try:
            weight_input = float(request.form.get('weight'))
        except (TypeError, ValueError):
            flash("Invalid weight input.")
            return redirect(url_for('main.add_weight'))
        unit = request.form.get('unit', 'kg')
        weight_kg = weight_input if unit == 'kg' else weight_input / 2.20462
        weight_entry = WeightEntry(user_id=user.id, weight_kg=weight_kg, date=datetime.utcnow())
        db.session.add(weight_entry)
        db.session.commit()
        flash("Weight entry added successfully.")
        return redirect(url_for('main.dashboard'))
    return render_template('main/add_weight.html')


@bp.route('/set_goal', methods=['GET', 'POST'])
@login_required
def set_goal():
    """
    Set or update a weight goal.
    """
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        try:
            goal_weight_input = float(request.form.get('goal_weight'))
        except (TypeError, ValueError):
            flash("Invalid goal weight.")
            return redirect(url_for('main.set_goal'))
        unit = request.form.get('unit', 'kg')
        goal_weight_kg = goal_weight_input if unit == 'kg' else goal_weight_input / 2.20462
        target_date_str = request.form.get('target_date')
        try:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.")
            return redirect(url_for('main.set_goal'))

        # Create or update the weight goal.
        goal = WeightGoal.query.filter_by(user_id=user.id).first()
        if goal:
            goal.goal_weight_kg = goal_weight_kg
            goal.target_date = target_date
        else:
            goal = WeightGoal(user_id=user.id, goal_weight_kg=goal_weight_kg, target_date=target_date)
            db.session.add(goal)
        db.session.commit()
        flash("Goal updated successfully.")
        return redirect(url_for('main.dashboard'))
    return render_template('main/set_goal.html')


@bp.route('/weight_history')
@login_required
def weight_history():
    """
    Display all historical weight entries.
    """
    user = User.query.get(session['user_id'])
    entries = WeightEntry.query.filter_by(user_id=user.id).order_by(WeightEntry.date.desc()).all()
    return render_template('main/weight_history.html', entries=entries, unit=user.unit_preference)


@bp.route('/bmi_history')
@login_required
def bmi_history():
    """
    Display historical BMI entries.
    """
    user = User.query.get(session['user_id'])
    entries = BMIEntry.query.filter_by(user_id=user.id).order_by(BMIEntry.date.desc()).all()
    return render_template('main/bmi_history.html', entries=entries)

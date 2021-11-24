"""
Routing for the home page
"""
from flask import render_template, Blueprint, request, session, redirect, url_for, g, flash

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':

        # If user already logged in, redirect to home page
        if 'USER_UNI' in session:
            return redirect(url_for('home.index'))
        else:
            return render_template('login.html')

    if request.method == 'POST':
        # Save user's UNI to session cookie
        unis = g.db.run_query('student_all_uni.sql')
        valid_uni = False
        for row in unis:
            if request.form.get('uni') == row.uni:
                session['USER_UNI'] = request.form.get('uni')
                valid_uni = True
                break

        if not valid_uni:
            flash('You don\'t have an account on New Vergil :(')

        return redirect(url_for('home.index'))


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Pop user's UNI from session cookie and redirect to home page
    if 'USER_UNI' in session:
        del session['USER_UNI']

    return redirect(url_for('home.index'))

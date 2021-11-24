"""
Classes page
"""
# Standard library imports
from math import ceil
from time import time as get_time
from datetime import time

# Third-party imports
from flask import render_template, request, redirect, flash, Blueprint, url_for, session, g

# Local application imports
from app.utils.helper import all_values_blank, replace_empty_with_none

bp = Blueprint('classes', __name__, url_prefix='/classes')
PAGE_SIZE = 3  # Search will be paginated with given page size


@bp.route('/')
def index():

    bldg_options = g.db.run_query('class_distinct_buildings.sql')
    dept_options = g.db.run_query('class_distinct_departments.sql')

    return render_template(
        'classes.html',
        bldg_options=bldg_options,
        dept_options=dept_options
    )


@bp.post('/query/<int:page>')
def query(page):
    """
    Perform a query based on the form submission
    """

    offset = page * PAGE_SIZE

    # Parse form submission
    form_data = dict(request.form)
    if 'days' in form_data:
        form_data['days'] = ''.join(request.form.getlist('days'))

    # The whole LIKE expression is a query paremeter
    if 'name' in form_data and form_data['name'] != '':
        form_data['name'] = f"%{form_data['name'].lower()}%"

    # Convert to SQL time format (e.g. 14:00:00)
    if 'begin_time' in form_data and form_data['begin_time'] != '':
        hour = int(form_data['begin_time'])
        form_data['begin_time'] = time(hour=hour).isoformat(timespec='auto')

    # Python None = SQL NULL
    form_data = replace_empty_with_none(form_data)

    # If form is not an empty dict (meaning user hit Search), save form data to session storage
    # Otherwise, user hit one of the page buttons
    # Restore form data form session storage to page through the same search results
    if not form_data:
        form_data = dict(session['class_search_form'])
    else:
        session['class_search_form'] = form_data

    if all_values_blank(form_data):
        count = g.db.run_query('class_all_count.sql', params={'offset': offset})[0][0]
        search_results = g.db.run_query('class_all.sql', params={'offset': offset})
    else:
        # Query parameters will have all the form data plus the offset
        query_params = {}
        query_params = form_data
        query_params['offset'] = offset

        # If none of the days are selected, they won't be part of the form
        # Need to add them as None manually
        if 'days' not in form_data:
            form_data['days'] = None

        count = g.db.run_query('class_search_count.sql', params=query_params)[0][0]
        search_results = g.db.run_query('class_search.sql', params=query_params)

    if 'USER_UNI' in session:
        query_params = {'uni': session['USER_UNI']}
        wishlisted = g.db.run_query('wishlist_query_by_uni.sql', params=query_params)
        wishlisted_id = [f"{w['course_id']}_{w['section']}" for w in wishlisted]
    else:
        wishlisted_id = []

    # Calculate maximum page using a query with COUNT (not efficient)
    max_page = ceil(count / PAGE_SIZE) - 1 if count != PAGE_SIZE else 0

    return render_template(
        'classes_search_results.html',
        search_results=search_results,
        search_results_count=count,
        current_page=page,
        max_page=max_page,
        wishlisted_id=wishlisted_id
    )


@bp.route('review/write/<course_id_section>')
def review_write(course_id_section):
    course_id, section = course_id_section.split('_')

    return render_template(
        'review_write.html',
        course_id=course_id,
        section=section
    )


@bp.route('review/read/<course_id_section>')
def review_read(course_id_section):
    # Get course name from course_id
    course_id, section = course_id_section.split('_')

    reviews = g.db.run_query(
        'class_all_reviews.sql',
        params={
            'course_id': course_id,
            'section': section
        })

    if reviews:
        course_name = f"{reviews[0]['course_id']} - {reviews[0]['course_name']}"
        instructor_first_name = reviews[0]['first_name']
        instructor_last_name = reviews[0]['last_name']
    else:
        course_name = ''
        instructor_first_name = ''
        instructor_last_name = ''

    return render_template(
        'review_read.html',
        review_for=course_name,
        reviews=reviews,
        review_category='class',
        instructor_first_name=instructor_first_name,
        instructor_last_name=instructor_last_name
    )


@bp.post('/review/post')
def post_review():

    if request.form['content'] == '':
        flash('ERROR: review cannot be empty')
    elif len(request.form['content']) > 2000:
        flash('ERROR: review cannot be longer than 2000 characters')
    else:
        query_params = {
            'content': request.form['content'],
            'uni': session['USER_UNI'],
            'section': request.form['section'],
            'course_id': request.form['course_id'],
        }

        g.db.run_query('class_add_review.sql', params=query_params)
        flash('Review posted successfully')

    return redirect(url_for('classes.index'))

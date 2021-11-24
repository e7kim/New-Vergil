"""
Instructors page
"""
# Standard library imports
from math import ceil

# Third-party imports
from flask import render_template, request, Blueprint, session, g

# Local application imports
from app.utils.helper import all_values_blank

bp = Blueprint('instructors', __name__, url_prefix='/instructors')

PAGE_SIZE = 3  # Search will be paginated with given page size


@bp.route('/')
def index():

    bldg_options = g.db.run_query('instructor_distinct_buildings.sql')
    dept_options = g.db.run_query('instructor_distinct_departments.sql')

    return render_template(
        'instructors.html',
        bldg_options=bldg_options,
        dept_options=dept_options
    )


@bp.post('/query/<int:page>')
def query(page):
    """
    Perform a query based on the form submission with pagination
    """
    offset = page * PAGE_SIZE
    form_data = dict(request.form)

    # If form is not an empty dict (meaning user hit Search), save form data to session storage
    # Otherwise, user hit one of the page buttons
    # Restore form data form session storage to page through the same search results
    if not form_data:
        form_data = dict(session['instructor_search_form'])
    else:
        session['instructor_search_form'] = form_data

    # If blank form was submitted, return all instructors
    if all_values_blank(form_data):
        count = g.db.run_query('instructor_all_count.sql', params={
                               'offset': offset})[0][0]
        search_results = g.db.run_query(
            'instructor_all.sql', params={'offset': offset})
    else:
        # The whole LIKE expression is a query paremeter
        if 'name' in form_data and form_data['name'] != '':
            form_data['name'] = f"%{form_data['name'].lower()}%"

        # Query parameters will have all the form data plus the offset
        query_params = {}
        query_params = form_data
        query_params['offset'] = offset

        count = g.db.run_query(
            'instructor_search_count.sql', params=query_params)[0][0]
        search_results = g.db.run_query(
            'instructor_search.sql', params=query_params)

    # Calculate maximum page using a query with COUNT (not efficient)
    max_page = ceil(count / PAGE_SIZE) - 1 if count != PAGE_SIZE else 0

    return render_template(
        'instructors_search_results.html',
        search_results=search_results,
        search_results_count=count,
        current_page=page,
        max_page=max_page
    )


@bp.route('review/read/<uni>')
def review_read(uni):

    reviews = g.db.run_query(
        'instructor_all_reviews_by_uni.sql', params={'uni': uni})

    if reviews:
        instructor_name = f"{reviews[0]['first_name']} {reviews[0]['last_name']}"
    else:
        instructor_name = ''

    return render_template(
        'review_read.html',
        review_for=instructor_name,
        reviews=reviews,
        review_category='instructor'
    )

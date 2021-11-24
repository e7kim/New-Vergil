"""
Wishlist page

It's a bit weird because no fancy JavaScript is used.
For example, if user clicks "add to wishlist" from
the classes page, then we need to output the same
search results that they saw on that page. The
reason is that we reuse the classes_search_results.html
template.
"""
# Third-party imports
from flask import render_template, redirect, flash, Blueprint, session, url_for, g

bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')


@bp.route('/')
def index():
    return render_template('wishlist.html')


@bp.route('/query', methods=['GET', 'POST'])
def query():
    # Query for the wishlist
    # Because we are returning the same template classes_search_results.html
    # Here, "search results" are actually the user's wishlist
    query_params = {'uni': session['USER_UNI']}
    search_results = g.db.run_query('wishlist_query_by_uni.sql', params=query_params)

    return render_template('wishlist_query_results.html', search_results=search_results)


@bp.route('/add/<course_section>', methods=['POST'])
def add(course_section):
    # Add to wishlist
    course_id, section = course_section.split('_')
    query_params = {
        'uni': session['USER_UNI'],
        'section': section,
        'course_id': course_id,
    }

    g.db.run_query('wishlist_add.sql', params=query_params)
    flash('Class added to wishlist')

    return redirect(url_for('wishlist.index'))


@bp.route('/remove/<course_section>', methods=['POST'])
def remove(course_section):
    # Remove from wishlist
    course_id, section = course_section.split('_')
    query_params = {
        'uni': session['USER_UNI'],
        'section': section,
        'course_id': course_id,
    }

    g.db.run_query('wishlist_remove.sql', params=query_params)
    flash('Class removed from wishlist')

    return redirect(url_for('wishlist.index'))

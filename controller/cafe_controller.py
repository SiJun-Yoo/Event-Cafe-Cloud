from flask import Blueprint, jsonify, render_template
from database import DB

bp = Blueprint('cafe', __name__)


@bp.route('/cafe/detail')
def routeCafeDetail():
    return render_template('cafeDetail.html')

@bp.route('/api/cafe/detail/<cafeId>')
def getCafeDetail(cafeId):
    cafes = DB.find_one('cafes', {'idx': int(cafeId)},{'_id':False})
    events = DB.list('event', {'cafe_id': cafeId},{'_id':False})
    reviews = []
    for event in events:
        review = DB.list('reviews', {'event_id': event['event_id']},{'_id':False})
        reviews.append(review)
    response = {
        'cafes':cafes,
        'reviews': reviews
    }
    return jsonify(response)

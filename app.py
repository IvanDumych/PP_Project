from os import abort

from flask import Flask, request, jsonify, abort
from pp_project import app, Session
from schemas import UserSchema, AudienceSchema
from pp_project.models import User, Audience, Reservation
from datetime import datetime

audience_schema = AudienceSchema(many=True)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'message': 'Hello World'})


schema = UserSchema()


# validation
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(405)
def wrong_date(e):
    return jsonify(error=str(e)), 405


def check_dates(date, date2, date3):
    if date2 <= date <= date3:
        abort(405, description="Invalid input of dates")


def compare_dates(date1, date2):
    if not date1 <= date2:
        abort(405, description="Invalid input of dates")


# users
@app.route('/user/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        abort(404, description="User not found")
    return UserSchema().dump(user)


@app.route('/user/', methods=['POST'])
def create_user():
    session = Session()

    data = request.get_json()

    try:
        user = User(**data)
    except:
        return jsonify({"Message": "Invalid input"}), 405

    user.hash_password()

    session.add(user)
    session.commit()

    return jsonify({"Success": "User has been created"}), 200


@app.route('/user/<int:user_id>/', methods=['PUT'])
def update_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        abort(404, description="User not found")

    data = request.get_json()
    try:
        if data.get('first_name', None):
            user.first_name = data['first_name']
        if data.get('second_name', None):
            user.second_name = data['second_name']
        if data.get('user_name', None):
            user.user_name = data['user_name']
        if data.get('password', None):
            user.password = data['password']
            user.hash_password()

    except:
        abort(405, description="Invalid input")

        # return jsonify({"Message": "Invalid input"}), 405

    session.commit()

    return jsonify({"Success": "User has been changed"}), 200


@app.route('/user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        abort(404, description="User not found")

    try:
        reservations = session.query(Reservation).filter_by(user_id=int(user_id)).all()
    except:
        reservations = []

    session.delete(user)
    for reservation in reservations:
        session.delete(reservation)

    session.commit()

    return jsonify({"Success": "User has been deleted"}), 200


# audiences
@app.route('/audience/', methods=['POST'])
def create_audience():
    session = Session()

    data = request.get_json()

    try:
        audience = Audience(**data)
    except Exception:
        abort(405, description="Invalid input")

    if not data['size'] > 0 and data['capacity'] > 0:
        abort(405, description="Invalid input")

    session.add(audience)
    session.commit()

    return jsonify({"Success": "Audience has been created"}), 200


@app.route('/audience/<int:audience_id>/', methods=['GET'])
def get_audience(audience_id):
    session = Session()
    try:
        audience = session.query(Audience).filter_by(id=int(audience_id)).one()
    except:
        abort(404, description="Audience not found")

    return AudienceSchema().dump(audience)


@app.route('/audience/', methods=['GET'])
def get_all_audience():
    session = Session()
    try:
        all_audience = session.query(Audience).all()
    except:
        abort(404, description="Audiences not found")

    result = audience_schema.dump(all_audience)
    return jsonify(result)


# reservations
@app.route('/reservation/', methods=['POST'])
def create_reservation():
    session = Session()

    data = request.get_json()
    try:
        user = session.query(User).filter_by(id=int(data.pop('user_id'))).one()
    except:
        abort(404, description="User not found")

    try:
        audience = session.query(Audience).filter_by(id=int(data.pop('audience_id'))).one()
    except:
        abort(404, description="Audience not found")

    d = datetime.strptime(data['from_date'], '%Y-%m-%d')
    data['from_date'] = d.date()

    d = datetime.strptime(data['to_date'], '%Y-%m-%d')
    data['to_date'] = d.date()

    compare_dates(data['from_date'], data['to_date'])

    try:
        reservations = session.query(Reservation).filter_by(audience_id=int(audience.id)).all()
    except:
        reservations = []

    for reserv_other in reservations:
        check_dates(data['from_date'], reserv_other.from_date, reserv_other.to_date)
        check_dates(data['to_date'], reserv_other.from_date, reserv_other.to_date)

    try:
        reservation = Reservation(**data, user_r=user,
                                  audience_r=audience)
    except:
        return jsonify({"Message": "Invalid input"}), 405

    session.add(reservation)
    session.commit()

    return jsonify({"Success": "Reservation has been created"}), 200


@app.route('/reservation/<int:reservation_id>/', methods=['PUT'])
def update_reservation(reservation_id):
    session = Session()
    try:
        reservation = session.query(Reservation).filter_by(id=int(reservation_id)).one()
    except:
        abort(404, description="Reservation not found")
    data = request.get_json()
    try:
        if data.get('from_date', None):
            d = datetime.strptime(data['from_date'], '%Y-%m-%d')
            reservation.from_date = d.date()

        if data.get('to_date', None):
            d = datetime.strptime(data['to_date'], '%Y-%m-%d')
            reservation.to_date = d.date()

        if data.get('audience_id', None):
            reservation.audience_id = data['audience_id']

    except Exception:
        return jsonify({"Message": "Invalid input"}), 405

    compare_dates(reservation.from_date, reservation.to_date)

    try:
        audience = session.query(Audience).filter_by(id=int(reservation.audience_id)).one()
    except:
        abort(404, description="Audience not found")

    try:
        reservations = session.query(Reservation).filter_by(audience_id=int(audience.id)).all()
    except:
        reservations = []

    for reserv_other in reservations:
        if reserv_other.id != reservation.id:
            check_dates(reservation.from_date, reserv_other.from_date, reserv_other.to_date)
            check_dates(reservation.to_date, reserv_other.from_date, reserv_other.to_date)

    session.commit()

    return jsonify({"Success": "Reservation has been changed"}), 200


@app.route('/reservation/<int:reservation_id>/', methods=['DELETE'])
def delete_reservation(reservation_id):
    session = Session()
    try:
        reservation = session.query(Reservation).filter_by(id=int(reservation_id)).one()
    except:
        abort(404, description="Reservation not found")

    session.delete(reservation)
    session.commit()

    return jsonify({"Success": "Reservation has been deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)

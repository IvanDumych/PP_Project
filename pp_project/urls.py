from os import abort
from flask import Flask, request, jsonify, abort
from flask.globals import session
from pp_project import app, Session, auth, bcrypt
from pp_project.schemas import ReservationSchema, UserSchema, AudienceSchema
from pp_project.models import User, Audience, Reservation
from datetime import datetime

audience_schema = AudienceSchema(many=True)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'message': 'Hello World'})


schema = UserSchema()


def auth_check(user_id, user_name):
    session = Session()

    user = session.query(User).filter_by(user_name=user_name).one()

    if int(user_id) != user.id:
        abort(403, description="Access forbiden")


@auth.verify_password
def verify_password(username, password):
    session = Session()
    try:
        user = session.query(User).filter_by(user_name=username).one()
    except:
        abort(404, description="User not found")

    return bcrypt.check_password_hash(user.password, password)


# validation


@app.errorhandler(404)
def forbiden(e):
    return jsonify(error=str(e)), 403


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
@auth.login_required
def get_user(user_id):
    session = Session()

    print(auth.current_user())

    auth_check(user_id, auth.current_user())

    user = session.query(User).filter_by(id=int(user_id)).one()

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
@auth.login_required
def update_user(user_id):
    auth_check(user_id, auth.current_user())

    session = Session()

    user = session.query(User).filter_by(id=int(user_id)).one()

    data = request.get_json()

    if data.get('first_name', None):
        user.first_name = data['first_name']
    if data.get('second_name', None):
        user.second_name = data['second_name']
    if data.get('user_name', None):
        user.user_name = data['user_name']
    if data.get('password', None):
        user.password = data['password']
        user.hash_password()

    session.commit()

    return jsonify({"Success": "User has been changed"}), 200


@app.route('/user/<int:user_id>/', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    session = Session()

    auth_check(user_id, auth.current_user())

    user = session.query(User).filter_by(id=int(user_id)).one()

    reservations = session.query(Reservation).filter_by(user_id=int(user_id)).all()

    session.delete(user)
    for reservation in reservations:
        session.delete(reservation)

    session.commit()

    return jsonify({"Success": "User has been deleted"}), 200


# audiences
@app.route('/audience/', methods=['POST'])
@auth.login_required
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
@auth.login_required
def get_audience(audience_id):
    session = Session()
    try:
        audience = session.query(Audience).filter_by(id=int(audience_id)).one()
    except:
        abort(404, description="Audience not found")

    return AudienceSchema().dump(audience)


@app.route('/audience/', methods=['GET'])
@auth.login_required
def get_all_audience():
    session = Session()

    all_audience = session.query(Audience).all()
    if len(all_audience) == 0:
        abort(404, description="Audiences not found")

    result = audience_schema.dump(all_audience)
    return jsonify(result)


# reservations
@app.route('/reservation/', methods=['GET'])
def get_reservation():
    session = Session()

    reservations = session.query(Reservation).all()

    result = ReservationSchema(many=True).dump(reservations)

    return jsonify(result)


@app.route('/reservation/', methods=['POST'])
@auth.login_required
def create_reservation():
    session = Session()

    data = request.get_json()
    try:
        user = session.query(User).filter_by(id=int(data.pop('user_id'))).one()
    except Exception:
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

    reservations = session.query(Reservation).filter_by(audience_id=int(audience.id)).all()

    for reserv_other in reservations:
        check_dates(data['from_date'], reserv_other.from_date, reserv_other.to_date)
        check_dates(data['to_date'], reserv_other.from_date, reserv_other.to_date)

    reservation = Reservation(**data, user_r=user,
                              audience_r=audience)

    session.add(reservation)
    session.commit()

    return jsonify({"Success": "Reservation has been created"}), 200


@app.route('/reservation/<int:reservation_id>/', methods=['PUT'])
@auth.login_required
def update_reservation(reservation_id):
    session = Session()
    try:
        reservation = session.query(Reservation).filter_by(id=int(reservation_id)).one()
    except:
        abort(404, description="Reservation not found")

    auth_check(reservation.user_id, auth.current_user())

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

    reservations = session.query(Reservation).filter_by(audience_id=int(audience.id)).all()

    for reserv_other in reservations:
        if reserv_other.id != reservation.id:
            check_dates(reservation.from_date, reserv_other.from_date, reserv_other.to_date)
            check_dates(reservation.to_date, reserv_other.from_date, reserv_other.to_date)

    session.commit()

    return jsonify({"Success": "Reservation has been changed"}), 200


@app.route('/reservation/<int:reservation_id>/', methods=['DELETE'])
@auth.login_required
def delete_reservation(reservation_id):
    session = Session()
    try:
        reservation = session.query(Reservation).filter_by(id=int(reservation_id)).one()
    except Exception:
        abort(404, description="Reservation not found")

    auth_check(reservation.user_id, auth.current_user())

    session.delete(reservation)
    session.commit()

    return jsonify({"Success": "Reservation has been deleted"}), 200

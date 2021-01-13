from pp_project.models import User, Audience, Reservation


def get_test_audience_data(location='Lviv',
                           size=22,
                           capacity=25):
    audience = {
        'location': location,
        'size': size,
        'capacity': capacity
    }
    return audience


def create_audience(session, data=None):
    if data is None:
        data = get_test_audience_data()
    audience = Audience(**data)
    session.add(audience)
    session.commit()
    return audience, data


def get_test_user_data(first_name='test_first_name',
                       second_name='test_second_name',
                       user_name='test_username',
                       password='test_password'):
    user = {
        'first_name': first_name,
        'second_name': second_name,
        'user_name': user_name,
        'password': password
    }
    return user


def create_user(session, data=None):
    if data is None:
        data = get_test_user_data()
    user = User(**data)
    user.hash_password()
    session.add(user)
    session.commit()
    return user, data


def get_test_reservation_data(from_date='2000-01-01',
                              to_date='2000-01-21',
                              user_id=1,
                              audience_id=1):
    reservation = {
        'from_date': from_date,
        'to_date': to_date,
        'user_id': user_id,
        'audience_id': audience_id
    }
    return reservation


def create_reservation(session, data=None):
    import datetime
    if data is None:
        data = get_test_reservation_data()
        data['from_date'] = datetime.date(2000, 1, 1)
        data['to_date'] = datetime.date(2000, 1, 21)
    else:
        from_date = [int(i) for i in data['from_date'].split('-')]
        to_date = [int(i) for i in data['to_date'].split('-')]
        data['from_date'] = datetime.date(from_date[0], from_date[1], from_date[2])
        data['to_date'] = datetime.date(to_date[0], to_date[1], to_date[2])
    reservation = Reservation(**data)
    session.add(reservation)
    session.commit()
    return reservation, data

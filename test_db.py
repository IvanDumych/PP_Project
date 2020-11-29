from datetime import date
from pp_project import Session
from pp_project.models import User, Audience, Reservation

session = Session()

user = User(
    id=1,
    first_name='Vitalik',
    second_name='Shkliarov',
    user_name='Rumaru001',
    password='qwerty'
)

audience = Audience(
    id=1,
    location='Lviv',
    size=22,
    capacity=25
)

reservation = Reservation(
    id=1,
    from_date=date(2020, 12, 11),
    to_date=date(2020, 12, 14),
    user_r=user,
    audience_r=audience
)

session.add(user)
session.add(audience)
session.add(reservation)

session.commit()
session.close()

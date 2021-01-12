from datetime import date
from pp_project import Session
from pp_project.models import User, Audience, Reservation

session = Session()

user = User(
    id=1,
    first_name='Vitalikfc',
    second_name='Shkliarovfc',
    user_name='Rumaru00fc',
    password='qwertyfc'
)

user2 = User(
    id=2,
    first_name='Vitalik2',
    second_name='Shkliarov2',
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

user = session.query(User).filter_by(id=1).one()

user.user_name = "Alex"

session.add(user)

session.commit()
session.close()
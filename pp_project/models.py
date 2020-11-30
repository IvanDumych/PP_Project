from pp_project import engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    reservations = relationship("Reservation")

    def __repr__(self):
        return f'<User(first_name="{self.first_name}", ' \
               f'second_name="{self.second_name}")>'


class Audience(Base):
    __tablename__ = 'audience'
    id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)

    reservations = relationship("Reservation")

    def __repr__(self):
        return f'<Audience(location={self.location}, ' \
               f'size={self.size})>'


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    user_id = Column(
        Integer, ForeignKey('user.id'), nullable=False
    )
    audience_id = Column(
        Integer, ForeignKey('audience.id'), nullable=False
    )

    user_r = relationship(
        User, foreign_keys=[user_id]
    )
    audience_r = relationship(
        Audience, foreign_keys=[audience_id]
    )

    def __repr__(self):
        return f'<Reservation(from_date="{self.from_date}", ' \
               f'to_date="{self.to_date}")>'


# Base.metadata.create_all(engine)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pp_project import engine
from flask_bcrypt import generate_password_hash, check_password_hash

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    reservations = relationship("Reservation")

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

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

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Useer(db.Model):

    __tablename__ = 'Useer'

    id = db.Column(db.Integer, primary_key=True)

    #__Useer_FIELDS__
    name = db.Column(db.String(255),  nullable=True)
    email = db.Column(db.String(255),  nullable=True)
    password = db.Column(db.String(255),  nullable=True)
    subscribed = db.Column(db.Boolean, nullable=True)

    #__Useer_FIELDS__END

    def __init__(self, **kwargs):
        super(Useer, self).__init__(**kwargs)


class Robot(db.Model):

    __tablename__ = 'Robot'

    id = db.Column(db.Integer, primary_key=True)

    #__Robot_FIELDS__
    robot_id = db.Column(db.Integer, nullable=True)
    robot_ip = db.Column(db.String(255),  nullable=True)
    robot_port = db.Column(db.Integer, nullable=True)
    robot_status = db.Column(db.String(255),  nullable=True)
    latitude = db.Column(db.String(255),  nullable=True)
    longitude = db.Column(db.String(255),  nullable=True)

    #__Robot_FIELDS__END

    def __init__(self, **kwargs):
        super(Robot, self).__init__(**kwargs)


class Robot_Motion_Plan(db.Model):

    __tablename__ = 'Robot_Motion_Plan'

    id = db.Column(db.Integer, primary_key=True)

    #__Robot_Motion_Plan_FIELDS__
    plan_status = db.Column(db.String(255),  nullable=True)
    plan = db.Column(db.Text, nullable=True)
    command_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Robot_Motion_Plan_FIELDS__END

    def __init__(self, **kwargs):
        super(Robot_Motion_Plan, self).__init__(**kwargs)



#__MODELS__END

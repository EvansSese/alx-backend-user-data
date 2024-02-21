#!/usr/bin/env python3
"""DB module
"""
from typing import Type
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """
    user_keys = ['id', 'email', 'hashed_password',
                 'session_id', 'reset_token']

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Function to add user into db"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Function to query for user by provided input"""
        for key in kwargs.keys():
            if key not in self.user_keys:
                raise InvalidRequestError

        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Function to update a user"""
        user_to_update = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key in self.user_keys:
                setattr(user_to_update, key, value)
            else:
                raise ValueError
        self._session.commit()

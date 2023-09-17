#!/usr/bin/env python3

"""DB module
"""
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

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """
        Add a new user to the database.

        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The User object representing the newly added user.
        """
        # Create a new User object
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session
        self._session.add(new_user)

        # Commit the session to save the user to the database
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find & return the first user in the db match the criteria.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The User object representing the first user found.

        Raises:
            NoResultFound: If no results match the criteria.
            InvalidRequestError: If an invalid query argument is passed.
        """

        try:
            # Query the database and filter based on the provided criteria
            user = self._session.query(User).filter_by(**kwargs).first()

            # If no user is found, raise NoResultFound
            if user is None:
                raise NoResultFound("No user found matching the criteria.")

            return user
        except NoResultFound:
            # Handle NoResultFound exception
            raise
        except InvalidRequestError:
            # Handle InvalidRequestError exception
            raise InvalidRequestError("Invalid query argument.")

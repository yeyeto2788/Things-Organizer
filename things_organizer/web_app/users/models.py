from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from things_organizer.extensions import database


class User(database.Model, UserMixin):
    """
    Model representation of the user table.

    """

    id = database.Column(
        database.Integer,
        primary_key=True
    )
    username = database.Column(
        database.String(80),
        unique=True,
        nullable=False
    )
    email = database.Column(
        database.String(120),
        unique=True,
        nullable=False
    )
    things = database.relationship(
        'Thing',
        backref='user',
        lazy='dynamic'
    )
    password_hash = database.Column(
        database.String
    )

    @property
    def password(self):
        """
        Property which is write-only so it will raise an exception if trying
        to access to it.

        Raises:
            AttributeError.

        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """
        Setter for the password hash.

        Args:
            password: Password to be hashed.

        """

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Validate hash of given password.

        Args:
            password: Password to be checked.

        Returns:
            True if it is correct else False.

        """

        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        """
        Get the user from the username given as parameter.

        Args:
            username: string with the username.

        Returns:
            User object.
        """

        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User %r>" % self.username

    def __unicode__(self):
        return self.username

from datetime import datetime

from sqlalchemy import desc

from things_organizer.extensions import database
from things_organizer.web_app.tags.models import Tag, tags


class Thing(database.Model):
    """
    Model representation of the thing table.

    """

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.Text, nullable=False)
    description = database.Column(database.String(300))
    unit = database.Column(database.String(100))
    quantity = database.Column(database.Integer)
    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), nullable=False
    )
    category_id = database.Column(
        database.Integer, database.ForeignKey("category.id"), nullable=False
    )
    storage_id = database.Column(
        database.Integer, database.ForeignKey("storage.id"), nullable=False
    )
    date = database.Column(database.DateTime, default=datetime.utcnow)
    _tags = database.relationship(
        "Tag", secondary=tags, backref=database.backref("things", lazy="dynamic")
    )
    category = database.relationship(
        "Category", backref=database.backref("things", lazy="dynamic")
    )
    storage = database.relationship(
        "Storage", backref=database.backref("things", lazy="dynamic")
    )

    @staticmethod
    def newest(num):
        """
        Get a given number of items based on the date created.

        Args:
            num: Integer for the number of things to be retrieved.

        Returns:
            List with things.
        """
        return Thing.query.order_by(desc(Thing.date)).limit(num)

    @property
    def tags(self):
        """
        Tags of the thing to be requested.

        Returns:
            All thing tags separated by coma.
        """
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        """
        Setter for thing tags splitting the text given as argument to
        generate a new tag for each slice on the string.

        Args:
            string: string to be split.

        """
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(",")]

    def __repr__(self):
        return f"<Thing {self.name}>"

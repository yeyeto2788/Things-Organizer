from things_organizer.extensions import database

tags = database.Table(
    'thing_tag',
    database.Column(
        'tag_id', database.Integer,
        database.ForeignKey('tag.id')
    ),
    database.Column(
        'thing_id', database.Integer,
        database.ForeignKey('thing.id')
    )
)


class Tag(database.Model):
    """
    Model representation of the tag table.

    """

    id = database.Column(
        database.Integer,
        primary_key=True
    )
    name = database.Column(
        database.String(25),
        nullable=False,
        unique=True,
        index=True
    )

    @staticmethod
    def get_or_create(name):
        """
        Method to get a tag by a given name or create it if does not exists.

        Args:
            name: Name for the tag

        Returns:
            Tag object

        """

        try:
            return Tag.query.filter_by(name=name).one()

        except Exception:
            return Tag(name=name)

    @staticmethod
    def all():
        """
        Get all tags from database.

        Returns:
            List with all tags on database.

        """

        return Tag.query.all()

    def __repr__(self):
        return self.name

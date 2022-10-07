from things_organizer.extensions import database


class Storage(database.Model):
    """
    Model representation of the storage table.

    """

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True, nullable=False)
    location = database.Column(database.String(120), nullable=False)
    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), nullable=False
    )

    @classmethod
    def get_user_storages(cls, user_id):
        """

        Args:
            user_id:

        Returns:

        """
        storages = []

        for storage in Storage.query.filter_by(user_id=user_id).all():
            storages.append((storage.id, storage.name))

        return storages

    def __repr__(self):
        return "<Storage {self.name}>"

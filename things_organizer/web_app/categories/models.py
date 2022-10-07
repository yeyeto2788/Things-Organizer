from things_organizer.extensions import database


class Category(database.Model):
    """
    Model representation of the category table.

    """

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True, nullable=False)
    user_id = database.Column(
        database.Integer, database.ForeignKey("user.id"), nullable=False
    )

    def __repr__(self):
        return f"<Category {self.name}>"

    @classmethod
    def get_user_categories(cls, user_id):
        """

        Args:
            user_id:

        Returns:

        """
        categories = []

        for category in Category.query.filter_by(user_id=user_id).all():
            categories.append((category.id, category.name))

        return categories

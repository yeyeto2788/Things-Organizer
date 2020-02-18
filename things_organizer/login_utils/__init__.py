from things_organizer.common.models import User


def load_user(user_id):
    """
    Retrieve the user from the database from a given id.

    Args:
        user_id: id of the user.

    Returns:
        User object.
    """
    return User.query.get(int(user_id))
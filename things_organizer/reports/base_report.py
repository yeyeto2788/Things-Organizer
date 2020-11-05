from things_organizer.web_app.categories.models import Category
from things_organizer.web_app.storages.models import Storage
from things_organizer.web_app.things.models import Thing


class BaseReport:
    file_directory = None
    file_name = None
    user_id = None

    def get_things(self):
        """
        Make a representation of the database to `.txt` file with all things
        in database.

        Returns:
            Path of the file created.

        """

        things = Thing.query.filter_by(user_id=self.user_id).all()
        column_names = [str(name).split('.')[1] for name in
                        Thing.__table__.columns]

        return column_names, things

    @classmethod
    def get_category(cls, category_id):
        """

        Args:
            category_id:

        Returns:

        """
        category = Category.query.filter_by(id=category_id).first()
        return category

    @classmethod
    def get_storage(cls, storage_id):
        """

        Args:
            storage_id:

        Returns:

        """
        storage = Storage.query.filter_by(id=storage_id).first()
        return storage

    def get_things_by_category(self, int_id):
        """
        Make a representation of the database to `.txt` file with all things
        in database filtered by category.

        Args:
            int_id: ID of the category to filter by.

        Returns:
            Path of the file created.

        """
        category = self.get_category(int_id)

        things = Thing.query.filter_by(
            user_id=self.user_id,
            category=category
        ).all()
        column_names = [str(name).split('.')[1] for name in
                        Thing.__table__.columns]
        column_names.remove('category_id')

        return column_names, things

    def get_things_by_storage(self, int_id):
        """
        Make a representation of the database to `.txt` file with all things
        in database filtered by storage.

        Args:
            int_id: ID of the storage to filter by.

        Returns:
            Path of the file created.

        """

        storage = self.get_storage(int_id)

        things = Thing.query.filter_by(user_id=self.user_id,
                                       storage=storage).all()
        column_names = [str(name).split('.')[1] for name in
                        Thing.__table__.columns]
        column_names.remove('storage_id')

        return column_names, things

    @staticmethod
    def _remove_data(things, lst_remove=None):
        """
        Static method to remove not needed items from the report.

        Args:
            things: Thing items on which removal will be applied.
            lst_remove: Items to be removed.

        Returns:
            Modified things parameter.

        """

        for data in things:
            data.pop('_sa_instance_state', None)
            data.pop('user_id', None)

            if lst_remove is not None:
                for str_remove in lst_remove:
                    if str_remove in data:
                        data.pop(str_remove, None)

        return things

    def write_file(self, lst_columns, things, str_title: str = None):
        """

        Returns:

        """
        raise NotImplementedError()

    def generate_by_category(self, category_id):
        pass

    def generate_by_storage(self, storage_id):
        pass

    def generate_all(self):
        pass

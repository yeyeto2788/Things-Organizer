"""

API end point for the things categories.

"""
from flask import jsonify
from flask_restful import Resource, abort

from things_organizer import utils
from things_organizer.data_management import common


class CategoriesAPI(Resource):
    """
    Class wrapper for the flask_restful.Resource in order to create the API.

    **NOTE:** By now the only method allow is `GET`, probably more methods will be added.

    """

    @staticmethod
    def get(int_id=None):
        """
        Find a category for a given ID, if no ID is provided it will return all available
        categories on table.

        Args:
            int_id: Id of the category to be searched.

        Returns:
            Response from jsonify function of flask.

        """
        dict_convert = {"data": 0}
        dict_inner = {}
        lst_values = []
        lst_columns = common.get_columns_from(
            common.TBL_CATEGORIES)

        if int_id is not None:
            lst_values = common.get_data_by_id(
                common.TBL_CATEGORIES, int_id)

        elif int_id is None:
            lst_values = common.get_all_data_from(
                common.TBL_CATEGORIES)

        try:
            if lst_values:

                if isinstance(lst_values[0], list):

                    for int_counter, row in enumerate(lst_values):
                        for int_inner, (column, value) in enumerate(zip(lst_columns, row)):
                            dict_inner[column] = value
                        dict_convert[int_counter + 1] = dict_inner

                    dict_convert['data'] = int_counter + 1

                else:
                    for int_inner, (column, value) in enumerate(zip(lst_columns, lst_values)):
                        dict_inner[column] = value
                    dict_convert[int_inner] = dict_inner

                    dict_convert['data'] = 1

            else:
                dict_convert['data'] = "None"

            return jsonify(str(dict_convert))

        except Exception as excerror:
            utils.debug("Error occurred on Category API.\nError: {}".format(excerror.__str__()))
            abort(404, error_message="Not found category '{}'.".format(int_id))

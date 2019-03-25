"""

API end point for the things categories.

"""
import flask_login

from flask import jsonify
from flask_restful import Resource, abort

import things_organizer
from things_organizer import utils


class ThingsAPI(Resource):
    """
    Class wrapper for the flask_restful.Resource in order to create the API.

    **NOTE:** By now the only method allow is `GET`, probably more methods will be added.

    """

    @staticmethod
    @flask_login.login_required
    def get(int_id=None):
        """
        Find a thing for a given ID, if no ID is provided it will return all available
        thing data on table.

        Args:
            int_id: Id of the thing to be searched.

        Returns:
            Response from jsonify function of flask.

        """
        dict_convert = {"data": 0}
        dict_inner = {}
        lst_values = []

        if int_id is not None:
            lst_values = things_organizer.db_models.Thing.query.filter_by(
                id=int_id, user_id=flask_login.current_user.id).first()

        elif int_id is None:
            lst_values = things_organizer.db_models.Thing.query.filter_by(
                user_id=flask_login.current_user.id).all()

        try:
            if lst_values:

                if isinstance(lst_values, list):

                    for int_inner, value in enumerate(lst_values):
                        dict_inner[int_inner] = {'id': value.id,
                                                 'name': value.name,
                                                 'description': value.description,
                                                 'unit': value.unit,
                                                 'quantity': value.quantity,
                                                 'category': value.category_id,
                                                 'storage': value.storage_id
                                                 }

                    dict_convert['things'] = dict_inner
                    dict_convert['data'] = len(lst_values)
                else:
                    dict_convert['id'] = lst_values.id
                    dict_convert['name'] = lst_values.name
                    dict_convert['description'] = lst_values.description
                    dict_convert['unit'] = lst_values.unit
                    dict_convert['quantity'] = lst_values.quantity
                    dict_convert['category'] = lst_values.category_id
                    dict_convert['storage'] = lst_values.storage_id
                    dict_convert['data'] = 1

            else:
                dict_convert['data'] = "None"

            return jsonify(str(dict_convert))

        except Exception as excerror:
            utils.debug("Error occurred on Things API.\nError: {}".format(excerror.__str__()))
            abort(404, error_message="Not found storage '{}'.".format(int_id))

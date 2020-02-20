import inspect
import time

import flask
import flask_login
from flask_restful import Resource

from things_organizer import utils
from things_organizer.web_app.categories.models import Category
from things_organizer.web_app.reports.forms import ReportForm
from things_organizer.reports.csv_report import CSV
from things_organizer.reports.txt_report import TXT
from things_organizer.web_app.storages.models import Storage


class ReportResource(Resource):
    @flask_login.login_required
    def get(self):
        """
        Use for generating the reports through a page.

        Returns:
            Flask template '_blank' modified based on the request.

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        form = ReportForm()
        report_types = [(1, 'CSV (.csv)'), (2, 'TXT (.txt)')]
        form.report_type.choices = report_types
        data_types = [(1, 'All items'), (2, 'All items by Category'), (3, 'All items by Storage')]
        form.data_type.choices = data_types
        categories = Category.get_user_categories(user_id=current_user)
        form.category.choices = categories
        storages = [(s.id, s.name) for s in Storage.query.filter_by(
            user_id=flask_login.current_user.id).all()]
        form.storage.choices = storages

        template_return = flask.render_template('reports.html', form=form)

        utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
        return flask.Response(template_return, mimetype='text/html')

    @flask_login.login_required
    def post(self):
        """
        Use for generating the reports through a page.

        Returns:
            Flask template '_blank' modified based on the request.

        """
        utils.debug("** {} - INI\t{} **\n".format(inspect.stack()[0][3],
                                                  time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

        form = ReportForm()
        report_types = [(1, 'CSV (.csv)'), (2, 'TXT (.txt)')]
        form.report_type.choices = report_types
        data_types = [(1, 'All items'), (2, 'All items by Category'), (3, 'All items by Storage')]
        form.data_type.choices = data_types
        categories = Category.get_user_categories(user_id=current_user)
        form.category.choices = categories
        storages = [(s.id, s.name) for s in Storage.query.filter_by(
            user_id=flask_login.current_user.id).all()]
        form.storage.choices = storages

        if form.validate_on_submit():
            report_type = form.report_type.data
            data_type = form.data_type.data
            category = form.category.data
            storage = form.storage.data

            report_name = '{}'.format(str(int(time.time())))

            if report_type == 1:
                report = CSV(report_name, flask_login.current_user.id)

            else:
                report = TXT(report_name, flask_login.current_user.id)

            if data_type == 1:
                report.get_all_things()

            else:
                if data_type == 2:
                    report.get_by_category(category)
                else:
                    report.get_by_storage(storage)

            template_return = flask.send_from_directory(report.file_directory,
                                                        report.file_name,
                                                        as_attachment=True)
            utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                      time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))

            return template_return

        else:
            template_return = flask.render_template('reports.html', form=form)

            utils.debug("** {} - END\t{} **\n".format(inspect.stack()[0][3],
                                                      time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
            return flask.Response(template_return, mimetype='text/html')

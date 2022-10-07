from flask_wtf import FlaskForm
from wtforms import SelectField


class ReportForm(FlaskForm):
    """
    FlaskForm for selecting the report to be printed.

    """

    report_type = SelectField(label="Select type of file", coerce=int)
    data_type = SelectField(label="Select data for report", coerce=int)
    category = SelectField(label="Select Category", coerce=int)
    storage = SelectField(label="Select Storage", coerce=int)

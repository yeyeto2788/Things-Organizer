"""

Report module for printing database information in different formats as CSV and TXT,
more options can be added in the future.

"""
import os

from things_organizer.reports.csv_report import ReportCSV
from things_organizer.reports.txt_report import ReportTXT


def get_report(file_name):
    report_types = {
        ".txt": ReportTXT,
        ".csv": ReportCSV
    }
    filename, file_extension = os.path.splitext(file_name)
    return report_types.get(file_extension)

"""
Utils module to use all over the application in order
not to repeat code.

Common conversions and so on.

"""
import os
import re
from zipfile import ZipFile


def sort_alphanumeric_list(lst_unsorted):
    """
    Sorts the given iterable in the way that is expected.

    Args:
        lst_unsorted: List of values to be sorted.

    Returns:
        Same list sorted.

    """

    convert = lambda text: int(text) if text.isdigit() else text  # noqa: E731
    alphanum_key = lambda key: [  # noqa: E731
        convert(character) for character in re.split("([0-9]+)", key)
    ]  # noqa: E731
    return sorted(lst_unsorted, key=alphanum_key)


def str_to_bln(str_value):
    """
    Convert a given string based on ('y', 'yes', 't', 'true', 'on', '1') into
    a boolean.

    An `ValueError` might be raised if not possible to convert string to
    boolean.

    Args:
        str_value: Value to be converted

    Returns:
        True if possible to convert. otherwise False.

    """

    val = str_value.lower()

    if val in ("true", "1", "t", "y", "yes", "on", "yeah", "yup", "certainly"):
        bln_return = True

    elif val in ("n", "no", "f", "false", "off", "0"):
        bln_return = False

    else:
        raise ValueError(f"{str_value} is not compatible to convert into boolean.")

    return bln_return


def zip_dir(zip_directory, zip_name, str_directory, bln_delete=0):
    """
    Generate a `.zip` folder with all content on a directory.

    Args:
        zip_directory: Directory where `.zip` file will be saved.
        zip_name: Name for the `.zip` folder.
        str_directory: Directory to look files from.
        bln_delete: Delete previous runs.

    Returns:
        Name of the `.zip` folder if generated, else empty string.

    """

    file_paths = []

    if not zip_name.endswith(".zip"):
        zip_name = f"{zip_name}.zip"

    for root, _directories, files in os.walk(str_directory):
        for filename in files:
            file_dir = os.path.join(root, filename)
            file_paths.append(file_dir)

    if file_paths:
        zip_filename = os.path.join(zip_directory, zip_name)

        with ZipFile(zip_filename, "w") as zip_file:
            for file in file_paths:
                folder_name = os.path.basename(os.path.dirname(file))
                zip_location = os.path.join(folder_name, os.path.basename(file))
                zip_file.write(file, zip_location)
        zip_file.close()

        if bln_delete:
            for str_file in file_paths:
                os.remove(str_file)
    else:
        zip_filename = ""

    return zip_filename

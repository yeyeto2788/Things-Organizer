"""

Module to generate QR labels with the data of a given Thing in the database.

"""
import os

import qrcode

from PIL import Image, ImageDraw

from things_organizer import utils


class QRLabel:
    """
    Class for generating the thing labels in QR code.

    Attributes:
        thing_name: Name to add on the label.
        thing_description: Description to add on the label.
        file_name: Name for the image generated.
        file_directory: Directory where labels are stored.
        storage_name: name of the storage.
        storage_location: Location of the storage.

    Quick example:
    ```
    label = QRLabel('SuperLabel', 'Sample description of a label')
    label.generate_label()
    ```

    """

    def __init__(self, str_name, str_description, s_name, s_location):
        """
        Constructor method for the QRLabel object.

        Args:
            str_name: Name of the label
            str_description: Description of the label.
            s_name: Storage name.
            s_location: Storage Location.

        """

        self.thing_name = str_name
        self.thing_description = str_description
        self.storage_name = s_name
        self.storage_location = s_location
        self.file_name = '{}.png'.format(str_name)
        self.file_directory = os.path.realpath(utils.LABEL_PATH)

        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

    def generate_label(self):
        """
        Method to generate the label from class properties using the qr-code module.

        """

        str_data = """Name:             {}
        Description:      {}
        Storage name:     {}
        Storage location: {}
        """.format(self.thing_name, self.thing_description,
                   self.storage_name, self.storage_location)

        final_file_name = os.path.join(self.file_directory, self.file_name)

        qr_img = qrcode.QRCode(version=1,
                               error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=10,
                               border=4)

        qr_img.add_data(str_data)
        qr_img.make(fit=True)
        img = qr_img.make_image(fill_color="black", back_color="white")

        with open('{}'.format(final_file_name), 'wb') as qr_img_file:
            img.save(qr_img_file)

        qr_image = Image.open(final_file_name)

        # Calculate new values for the label
        base_width = 350
        width_percent = (base_width / float(qr_image.size[0]))
        height_size = int((float(qr_image.size[1]) * float(width_percent)))

        # Resize qr image since default gives 570x570px
        qr_image = qr_image.resize((base_width, height_size), Image.ANTIALIAS)

        lst_data = str_data.split('\n')

        # Final image with text
        bg_width = 384
        bg_height = base_width + (len(lst_data) * 10)
        bg_image = Image.new("1", [bg_width, bg_height], "white")
        drawing = ImageDraw.Draw(bg_image)

        # Fill background image with the text on the label.
        for int_index, line in enumerate(lst_data):
            add_height = int_index * 10
            final_text = line.replace('\n', '').lstrip()
            drawing.text((10, base_width + add_height), final_text, fill='black')

        final_position = int((bg_width - base_width) / 2)
        # Add qr image on background image and save it.
        bg_image.paste(qr_image, (final_position, 0))
        self.file_name = 'label-{}'.format(self.file_name)
        bg_image.save(os.path.join(self.file_directory, self.file_name))

import os

import qrcode
from qrcode.image.pure import PymagingImage

from things_organizer import utils


class QRLabel:

    def __init__(self, str_name, str_description):
        self.thing_name = str_name
        self.thing_description = str_description
        self.file_name = '{}.png'.format(str_name)
        self.file_directory = os.path.realpath(utils.LABEL_PATH)

        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)

    def generate_label(self):
        str_data = "Name: {}\nDescription: {}"

        final_file_name = os.path.join(self.file_directory, self.file_name)

        qr_img = qrcode.QRCode(version=1,
                               error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=10,
                               border=4, image_factory=PymagingImage)

        qr_img.add_data(str_data)
        qr_img.make(fit=True)
        img = qr_img.make_image(fill_color="black", back_color="white")

        with open('{}'.format(final_file_name), 'wb') as qr_img_file:
            img.save(qr_img_file)

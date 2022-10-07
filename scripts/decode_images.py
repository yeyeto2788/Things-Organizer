"""
Simple script to decode qr_labels generated by the application.
"""

import os

from PIL import Image
from pyzbar.pyzbar import decode

from things_organizer.constants import LABEL_PATH

for file in os.listdir(LABEL_PATH):
    print(f"\nReading '{file}'")
    data = decode(Image.open(os.path.join(LABEL_PATH, file)))
    print(f"Raw data: {data}")

    lst_data = data[0][0].decode("utf-8").split("\n")

    for line in lst_data:
        final_text = line.replace("\n", "").lstrip()
        print(final_text)

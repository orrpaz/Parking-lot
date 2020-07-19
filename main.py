import argparse
import os
import ocrspace
import Database
import logging
import re
from Configuration import readconfig


api_key = readconfig().get("api_key")
public_transport_last_digits = ['25', '26']
last_digits_prohibited = ['85', '86', '87', '88', '89', '00']
plate_lens = [7, 8]
divisor = 7
logging.basicConfig(filename='parking_info.log', level=logging.INFO)


def is_public_transport(license_plate):
    # check 2 last digit, return true if the last digit is 25/26
    return license_plate[-2:] in public_transport_last_digits


def is_last_two_digits_prohibit(license_plate):
    return len(license_plate) == 7 and license_plate[-2:] in last_digits_prohibited


def is_gas_vehicle(license_plate):
    license_plate = [int(digit) for digit in license_plate]
    return len(license_plate) in plate_lens and sum(license_plate) % divisor == 0


def edit_license_plate(license_plate):
    license_plate = license_plate.split("\r\n")[0]
    license_plate = re.sub('[,\'\\n".\\r;:!\s+?_\-—•]', '', license_plate)
    return license_plate


def is_valid_to_park(license_plate):
    # assume that there is one reason to prohibit.
    # if vehicles is public transportation and operated by gas, the reason will written to DB and log depends
    # on the following order: military_and_law,Public transportation, Operated by gas,
    # Last digits are 85/86/87/88/89/00

    info = "Allow to park"
    allow = True
    if is_military_and_law(license_plate):
        allow = False
        info = "Military and law"
    elif is_public_transport(license_plate):
        allow = False
        info = "Public transportation"
    elif is_gas_vehicle(license_plate):
        allow = False
        info = "Operated by gas"
    elif is_last_two_digits_prohibit(license_plate):
        allow = False
        info = "Last digits are 85/86/87/88/89/00"
    logging.info(license_plate + " " + info)
    query = "INSERT INTO parking.log (lisence,allowed,info) VALUES (%s,%s,%s)"
    val = (license_plate, str(allow), info)
    Database.insert_db(query, val)


def is_military_and_law(license_plate):
    return re.search("[a-zA-Z]", license_plate)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pictures_directory', type=str)
    args = parser.parse_args()
    Database.create_db()
    api = ocrspace.API(api_key=api_key)
    path = args.pictures_directory
    for filename in os.listdir(path):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.pdf', '.gif', '.bmp', '.tif')):
            license_plate = api.ocr_file(path + "/" + filename)
            license_plate = edit_license_plate(license_plate)
            if license_plate:
                is_valid_to_park(license_plate)
            else:
                logging.info("Can't extract information from image")
        else:
            logging.info("Can't extract information from file")


if __name__ == "__main__":
    main()

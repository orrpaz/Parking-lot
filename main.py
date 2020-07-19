import argparse
import os
import ocrspace
import DB
import logging
import re

# directory = "resources/negative"
api_key = 'be5e6db88388957'
public_transport_last_digits = ['25', '26']
last_digits_prohibited = ['85', '86', '87', '88', '89', '00']
car_plate_lens_prohibited = [7, 8]
divisor = 7
logger = logging.getLogger()


def is_public_transport(car):
    # check 2 last digit, return true if the last digit is 25/26
    return car[-2:] in public_transport_last_digits


def is_last_two_digits_prohibit(car):
    return len(car) == 7 and car[-2:] in last_digits_prohibited


def is_gas_vehicle(car):
    car = [int(digit) for digit in car]
    return len(car) in car_plate_lens_prohibited and sum(car) % divisor == 0


def edit_license_plate(car_details):
    car_details = car_details.strip()
    car_details = re.sub('[,\'\\n".\\r;:!\s+?_\-—•]', '', car_details)
    return car_details


def is_valid_to_park(car_plate):
    info = "allow to park"
    allow = True
    if is_military_and_law(car_plate):
        allow = False
        info = "Military and law"
    elif is_gas_vehicle(car_plate):
        allow = False
        info = "operated by gas"
    elif is_last_two_digits_prohibit(car_plate):
        allow = False
        info = "last digits are 85/86/87/88/89/00"
    elif is_public_transport(car_plate):
        allow = False
        info = "Public transportation"
    logger.info(car_plate + info)
    query = "INSERT INTO parking.log (lisence,allowed,info) VALUES (%s,%s,%s)"
    val = (car_plate, str(allow), info)
    DB.insert_db(query, val)


def is_military_and_law(car_details):
    return re.search("[a-zA-Z]", car_details)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pictures_directory', type=str)
    args = parser.parse_args()
    DB.create_db()
    api = ocrspace.API(api_key=api_key)
    path = args.pictures_directory
    for filename in os.listdir(path):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.pdf', '.gif', '.bmp', '.tif')):
            car_plate = api.ocr_file(path + "/" + filename)
            car_plate = edit_license_plate(car_plate)
            if car_plate:
                is_valid_to_park(car_plate)
            else:
                logger.info("Can't extract information from image")
        else:
            logger.info("Can't extract information from file")


if __name__ == "__main__":
    main()

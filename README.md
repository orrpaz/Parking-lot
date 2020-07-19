# Parking-lot

## Installations

First, download and install MySQL from the MySQL's official
[MySQL Server](https://dev.mysql.com/downloads/mysql/). You need to install the MySQL server to follow this tutorial. 

Next, you have to install mysql.connector for Python. 
We need mysql.connector to connect Python Script to the MySQL database.
Use the package manager pip to install 
**MySQL-connector-python**
```bash
pip install MySQL-connector-python
```
Also, you need to install Ocrspace's SDK to use Ocrspace API.
```bash
pip install ocrspace
```
after you install this packages, yuo will need to genatrate OCI API KEY From
[ocrspace website](https://ocr.space/ocrapi)
Insert your API Key to **config.properties**

Insert your user data of MySQLServer (**user and password**) and API KEY that you genarate to **config.properties**

## Usage

The program get as an argument path to directory which contains images for
decoding.
I added images as an example in resource directory.

Run in Shell:
```bash
python3 main.py <path to directory> 
```

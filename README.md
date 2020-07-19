# Parking-lot

## Installations
First, You must to install mysql server in computer
[MySQL Server](https://dev.mysql.com/downloads/mysql/)


Use the package manager pip to install **ocrspace** and **MySQL-connector-python**
```bash
pip install MySQL-connector-python
```
```bash
pip install ocrspace
```

You need to insert your user data of MySQLServer (**user and password**) to **config.properties**

## Usage

The program get as an argument path to directory which contains images for
decoding.
I added images as an example in resource directory.

Run in Shell:
```bash
python3 main.py <path to directory> 
```

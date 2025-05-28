# T-Global Product Parser
Parses data sheet of t global product and enters relevant information into the databasee.

## Description of each file
- db_models.py: This file contains the ORM that corresponds to the database table. It also initializes the data base engine and makes the connection with the Cloud SQL
- product_pdf_reader.py: This file has the pdf reader that will parse the tglobal product information (good as of 05/28/2025)
- insert_product.py: Inserts the product read into the cloud sql database. It'll make updates to existing products, features, attributes

## software requirements

- Python 3
- pdfplumber
- sqlalchemy >= 2.0

## How to use
1. Put the above 3 files in cloud shell directory.
2. Put the data sheet to be read in cloud shell and take down the relative path and put in the parameter of the `read_pdf()` method at the bottom of `insert_product.py`
3. Fill in `INSTANCE_CONNECTION_NAME`, `DB_USER`, `DB_PASS`, and `DB_NAME` variables with the Cloud SQL information in `db_models.py`
4. Run `insert_product.py`

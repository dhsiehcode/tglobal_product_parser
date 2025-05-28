
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, MetaData, inspect, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker, Session
from sqlalchemy import Column, String, Integer, Text, Boolean, Float


class Base(DeclarativeBase):
    pass


class ORM_Producer(Base):
    __tablename__ = 'producers'
    producer_id = Column(Integer, primary_key=True)
    producer_name = Column(String, nullable=False)

class ORM_Category(Base):
    __tablename__ = 'product_categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)

class ORM_Feature(Base):
    __tablename__ = 'features'
    feature_id = Column(Integer, primary_key=True)
    feature_description =  Column(Text)

class ORM_Application(Base):
    __tablename__ = 'applications'
    application_id = Column(Integer, primary_key=True)
    application_name = Column(String)

class ORM_Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('product_categories.category_id'), nullable=False)
    producer_id = Column(Integer, ForeignKey('producers.producer_id'), nullable=False)
    model_id = Column(String)
    description = Column(Text)
    pdf_url = Column(String)
    tables_url = Column(String)
    rohs_compliant = Column(Boolean)
    reach_compliant = Column(Boolean)
    ul_comparable = Column(Boolean)

    product_type = relationship('ORM_Category')    
    producer = relationship('ORM_Producer')

class ORM_ProductFeature(Base):
    __tablename__ = "product_features"
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True, autoincrement=False)
    feature_id = Column(Integer, ForeignKey('features.feature_id'), primary_key=True, autoincrement=False)
    
    product = relationship('ORM_Product')
    feature = relationship('ORM_Feature')

class ORM_ProductApplication(Base):
    __tablename__ = "product_applications"
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True, autoincrement=False)
    feature_id = Column(Integer, ForeignKey('applications.application_id'), primary_key=True, autoincrement=False)

class ORM_ProductAttribute(Base):
    __tablename__ = 'product_attributes'
    attribute_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)  # E.g., 'float', 'int', 'string'
    unit = Column(String, nullable=True)
    test_method = Column(String, nullable = True)


class ORM_AttributeValue(Base):
    __tablename__ = 'attribute_values'
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True, autoincrement=False)
    attribute_id = Column(Integer, ForeignKey('product_attributes.attribute_id'), primary_key=True, autoincrement=False)
    value = Column(String, nullable=True)  # store as string to handle multiple data types
    min_value = Column(Float, nullable=True)
    include_min = Column(Boolean, nullable=True)
    max_value = Column(Float, nullable=True)
    include_max = Column(Boolean, nullable=True)
    tolerance_value = Column(String)

    product = relationship('ORM_Product')
    attribute = relationship('ORM_ProductAttribute')


from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
from sqlalchemy import inspect

def get_all_tables(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    for table_name in tables:
        print(f"Table: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            col_name = column["name"]
            col_type = column["type"]
            print(f"  - {col_name} ({col_type})")


# Create a Cloud SQL Connector object
connector = Connector()

# Replace with your actual values
INSTANCE_CONNECTION_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_NAME = ""

# Function that returns a pg8000 connection
def getconn():
    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )

#engine = create_engine('sqlite:///test_products.db', echo=True)

engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Create a session
session = Session(engine)
#session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

## uncomment below line to test if it is successful
#get_all_tables(engine)


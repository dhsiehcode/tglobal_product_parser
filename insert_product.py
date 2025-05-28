from product_pdf_reader import Attribute, ProductWithAttributes, create_product_object

from db_models import  ORM_Product, ORM_ProductAttribute, ORM_AttributeValue, ORM_Category, ORM_Producer, ORM_Feature, ORM_ProductFeature
from db_models import session
from product_pdf_reader import read_pdf





def insert_attribute(attribute : Attribute, product_id : int):

    ## adds a attirbute to it's associated product, assumes product already exists

    ## check if the specific attribute with the name, unit, test method, exists

    attribute_query_res = session.query(ORM_ProductAttribute).filter(
        ORM_ProductAttribute.name == attribute.name, 
        ORM_ProductAttribute.unit == attribute.unit,
        ORM_ProductAttribute.test_method == attribute.test_method
        ).all()
    
    ## this attribute does not exist
    if len(attribute_query_res) == 0:

        new_product_attribute = ORM_ProductAttribute(
            name = attribute.name,
            data_type = attribute.data_type,
            unit = attribute.unit,
            test_method = attribute.test_method
        )
        session.add(new_product_attribute)
        session.commit()
        product_attribute_id = new_product_attribute.attribute_id
    
    else:
        product_attribute_id = attribute_query_res[0].attribute_id

    ## now we have the id for the entry in the product attribute table,
    ## we create an entry in the attributes value table

    attribute_value = ORM_AttributeValue(
        product_id = product_id,
        attribute_id = product_attribute_id,
        value = attribute.value,
        min_value = attribute.min,
        include_min = attribute.include_min,
        max_value = attribute.max,
        include_max = attribute.include_max,
        tolerance_value = attribute.tolerance
    )

    session.merge(attribute_value)
    session.commit()

    return attribute_value.attribute_id


def insert_feature(feature, product_id):

    ## check if feature exists

    feature_query_res = session.query(ORM_Feature).filter(
        ORM_Feature.feature_description == feature
    ).all()

    if len(feature_query_res) == 0:
        new_feature = ORM_Feature(feature_description = feature)
        session.add(new_feature)
        session.commit()
        feature_id = new_feature.feature_id
    else:
        feature_id = feature_query_res[0].feature_id

    
    new_product_feature = ORM_ProductFeature(
        product_id = product_id,
        feature_id = feature_id
    )

    session.merge(new_product_feature)
    session.commit()
    


def insert_product(product : ProductWithAttributes):

    ## check if the product with the same model_id exists

    products_query_res = session.query(ORM_Product).filter(
        ORM_Product.model_id == product.model_id
    ).all()

    ## if product already exists, we don't insert (for now, maybe update it for later).


    

    ## find or create category as necessary

    category_query_res = session.query(ORM_Category).filter_by(category_name = product.category).all()

    if len(category_query_res) == 0:

        new_category = ORM_Category(category_name = product.category)
        session.add(new_category)
        session.commit()
        category_id = new_category.category_id
        
    else:
        category_id = category_query_res[0].category_id
    
    ##　find or create producer as necessary
         
    producer_query_res = session.query(ORM_Producer).filter_by(producer_name = product.producer).all()

    if len(producer_query_res) == 0:
        ## create this producer
        new_producer = ORM_Producer(producer_name = product.producer)
        session.add(new_producer)
        session.commit()
        producer_id = new_producer.producer_id
    else:
        producer_id = producer_query_res[0].producer_id


    ##　create product

    
    if  len(products_query_res) == 0:
        

        orm_product = ORM_Product(
            category_id = category_id,
            producer_id = producer_id,
            model_id = product.model_id,
            description = product.description,
            pdf_url = product.pdf_url,
            tables_url = product.table_url,
            rohs_compliant = product.rohs_compliant,
            reach_compliant = product.reach_compliant,
            ul_comparable = product.ul_comparable
        )

        session.add(orm_product)
        session.commit()

        orm_product_id = orm_product.product_id
    
    else:

        orm_product_id = products_query_res[0].product_id

    ## insert feature

    for feature in product.features:
        insert_feature(feature, orm_product_id)

    ## insert attribute

    for attribute in product.attributes:
        insert_attribute(attribute, orm_product_id)


if __name__ == '__main__':


    product = read_pdf("product_pdfs/TG-AD75_Ultra_Soft_Thermal_Pad.pdf")


    insert_product(product)


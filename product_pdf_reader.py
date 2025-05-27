import pdfplumber


class Attribute():

    def __init__(self, name, unit, values, tolerance, test_method):

        ## first enter name
        ## if name is None type, if will be ignored (or entered as inches?)
        if name is None:
            self.name = 'thickness'
        else:
            self.name = name.lower() ## convert to lower case
        

        ## get the unit, if it is '-', there is no unit
        if unit == '-':
            self.unit = None
        else:
            self.unit = self.check_and_convert_superscript(unit)

        ## get the values, if value contains '~', it is a range. Or check if it is <, >, ≤, or ≥

        values = self.check_and_convert_superscript(values)

        if "~" in values:
            value_range = values.split("~")
            self.min = value_range[0]
            self.include_min = True
            self.max = value_range[1]
            self.include_max = True

            self.data_type = 'float'
        
        elif "<" in values:

            self.data_type = 'float'
            
            if values.find("<") == 0:
                self.max = values.split("<")[0]
                self.include_max = False
                self.min = None
                self.include_min = False
            else:
                self.min = values.split("<")[0]
                self.include_min = False
                self.max = None
                self.include_max = False

        elif ">" in values:

            self.data_type = 'float'

            if values.find(">") == 0:
                self.min = values.split(">")[0]
                self.include_min = False
                self.max = None
                self.include_max = False
            else:
                self.max = values.split(">")[0]
                self.include_max = False
                self.min = None
                self.include_min = False

        elif "≥" in values:

            self.data_type = 'float'

            if values.find("≥") == 0:
                self.min = values.split("≥")[0]
                self.include_min = True
                self.max = None
                self.include_max = False
            else:
                self.max = values.split("≥")[0]
                self.include_max = True
                self.min = None
                self.include_min = False
        
        else:
            
            self.min = False
            self.include_min = False
            self.max = False
            self.include_max = False

            

            ## attempt to convert type to float, or string
            try:
                self.value = float(values)
                self.data_type = 'float'
            except ValueError:
                self.value = values
                self.data_type = 'string'
        

        ## get the tolerance 
        ## store tolerance value as string

        if "-" in tolerance: ## no tolerance if "-" is present
            self.tolerance = None
        else:

            self.tolerance = "±" + tolerance
        

        ## get the test method

        if "-" in test_method:

            self.test_method = None

        else:

            self.test_method = test_method

    ## assumes that the super script is at he end. this means no values such as 10^12 - 10
    def check_and_convert_superscript(self, str):
        output_str = ''
        ## use a hash table for look up
        unicode_to_num = {'\u00B9': '1','\u00B2': '2',  '\u00B3': '3', '\u2074':'4', '\u2075':'5', '\u2076':'6','\u2077':'7','\u2078':'8','\u2079':'9'}

        ## identify indices that are exponents
        start_of_superscript = -1
        
        for i in range(len(str)):

            if str[i] in unicode_to_num:
                start_of_superscript = i
                break


        if start_of_superscript == -1:
            output_str = str
        else:

            output_str += str[:start_of_superscript]
            output_str += '^'
            output_str += '('

            for i in range(start_of_superscript, len(str)):

                output_str += unicode_to_num[str[i]]

            output_str  += ')'
        
            
        return output_str


class ProductWithAttributes():

    def __init__(self, category, producer, model, description, pdf_url, tabel_url, reach_compliant, rohs_compliant, ul_comparable, attributes):
        ...

def read_properties(pdf_file):

    ## get the page. since we only have 1 page we get the only one
    page = pdf_file.pages[0]

    tables = page.extract_table()

    rows = tables[1:]

    attributes = []

    for row in rows:

        attributes.append(Attribute(name=row[0], unit=row[1], values=row[2], tolerance=row[3], test_method=row[4]))

    return attributes
        
def read_basic_info(pdf_file):

    page = pdf_file.pages[0]

    extracted_text = page.extract_text()

    lines = extracted_text.split("\n")

    ## line 2 is the name of the product
    product_model_id = lines[1]

    ## line 3 is the product category
    product_category = lines[2]

    ## line 4 is the compliance. Assume compliance / certification comes in pairs of two words. 
    if "REACH Compliant" in lines[3]:
        reach_compliant = True
    else:
        reach_compliant = False

    if "RoHS Complint" in lines[3]:
        rohs_compliant = True
    else:
        rohs_compliant = False

    if "UL Comparable" in lines[3]:
        ul_comparable = True
    else:
        ul_comparable = False


    ## 
    producer = "tglobal"

    ## 
    product_description = ""
    return product_category, producer, product_model_id, product_description, reach_compliant, rohs_compliant, ul_comparable

    ## create a product object
def create_product_object(pdf_file):

    product_category, producer, product_model_id, product_description, reach_compliant, rohs_compliant, ul_comparable = read_basic_info(pdf_file)
    product_attributes = read_properties(pdf_file)

    product = ProductWithAttributes(product_category, producer, product_model_id, product_description, "", "" , reach_compliant, rohs_compliant,
                                    ul_comparable, product_attributes)
    

    return product


file_name = ""  # a t global data sheet

with pdfplumber.open(file_name) as pdf:
    

    product = create_product_object(pdf)

    





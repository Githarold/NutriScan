from bs4 import BeautifulSoup

def parse_nutritional_info_with_error_handling(xml_data):
    # Parsing the XML data using BeautifulSoup
    soup = BeautifulSoup(xml_data, 'xml')

    # Checking for the presence of the result code and message
    result_code_tag = soup.find('CODE')
    result_msg_tag = soup.find('MSG')

    # If the result code and message are found, check for errors
    if result_code_tag and result_msg_tag:
        result_code = result_code_tag.text
        result_msg = result_msg_tag.text

        # Error handling based on result code
        if result_code != "INFO-000":
            return {"error": True, "code": result_code, "message": result_msg}

    # Extracting the required nutritional information and converting to float
    calories = float(soup.find('NUTR_CONT1').text)
    carbohydrates = float(soup.find('NUTR_CONT2').text)
    protein = float(soup.find('NUTR_CONT3').text)
    fat = float(soup.find('NUTR_CONT4').text)
    sugars = float(soup.find('NUTR_CONT5').text)
    sodium = float(soup.find('NUTR_CONT6').text)
    cholesterol = float(soup.find('NUTR_CONT7').text)
    saturated_fat = float(soup.find('NUTR_CONT8').text)
    trans_fat = float(soup.find('NUTR_CONT9').text)

    # Storing the data in a dictionary
    nutritional_info = {
        'calories': calories,
        'carbohydrates': carbohydrates,
        'protein': protein,
        'fat': fat,
        'sugars': sugars,
        'sodium': sodium,
        'cholesterol': cholesterol,
        'saturated_fat': saturated_fat,
        'trans_fat': trans_fat
    }

    print(nutritional_info)
    return {"error": False, "nutritional_info": nutritional_info}

xml_data_success = '''
<I2790>
    <row id="0">
        <NUTR_CONT8>6</NUTR_CONT8>
        <NUTR_CONT9>0.2</NUTR_CONT9>
        <NUTR_CONT4>25.8</NUTR_CONT4>
        <NUTR_CONT5>21.2</NUTR_CONT5>
        <NUTR_CONT6>1535.83</NUTR_CONT6>
        <NUTR_CONT7>193.4</NUTR_CONT7>
        <NUTR_CONT1>595.61</NUTR_CONT1>
        <NUTR_CONT2>44.9</NUTR_CONT2>
        <NUTR_CONT3>45.9</NUTR_CONT3>
    </row>
</I2790>
'''

# Testing the function with the corrected implementation
parse_nutritional_info_with_error_handling(xml_data_success)

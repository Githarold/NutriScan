import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv


class Parser:
    def __init__(self):
        # Load API KEY
        load_dotenv(find_dotenv())
        self.nut_api_key = os.getenv("NUT_TOKEN")

    def get_info_openapi(self, food_name):
        # Use openapi to get nutrient xml data
        url = (
            f"http://openapi.foodsafetykorea.go.kr/api/{self.nut_api_key}"
            f"/I2790/xml/1/1/DESC_KOR={food_name}"
        )

        response = requests.get(url)
        xml_data = response.content

        # Parse XML data using BeautifulSoup
        soup = BeautifulSoup(xml_data, "xml")

        # Check if result code and message are present
        result_code_tag = soup.find("CODE")
        result_msg_tag = soup.find("MSG")

        if result_code_tag and result_msg_tag:
            result_code = result_code_tag.text
            result_msg = result_msg_tag.text

            # Error handling based on result code
            if result_code != "INFO-000":
                return {"error": True, "code": result_code, "message": result_msg}

        # Extract and convert necessary nutrient information to float
        def get_nutrient_value(tag_name):
            tag = soup.find(tag_name)
            return float(tag.text) if tag and tag.text else 0.0

        calories = get_nutrient_value("NUTR_CONT1")
        carbohydrates = get_nutrient_value("NUTR_CONT2")
        protein = get_nutrient_value("NUTR_CONT3")
        fat = get_nutrient_value("NUTR_CONT4")
        sugars = get_nutrient_value("NUTR_CONT5")
        sodium = get_nutrient_value("NUTR_CONT6")
        cholesterol = get_nutrient_value("NUTR_CONT7")
        saturated_fat = get_nutrient_value("NUTR_CONT8")
        trans_fat = get_nutrient_value("NUTR_CONT9")

        # Store the data in a dictionary, changing keys to Korean
        nutritional_info = {
            "칼로리": calories,
            "탄수화물": carbohydrates,
            "단백질": protein,
            "지방": fat,
            "당류": sugars,
            "나트륨": sodium,
            "콜레스테롤": cholesterol,
            "포화지방": saturated_fat,
            "트랜스지방": trans_fat,
        }

        return {"error": False, "nutritional_info": nutritional_info}

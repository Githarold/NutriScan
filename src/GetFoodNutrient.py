import os, requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

class Parser:
    
    def __init__(self):
        
        # API KEY 가져옴
        load_dotenv(find_dotenv())
        self.nut_api_key = os.getenv('NUT_TOKEN')
    
    def get_info_openapi(self, food_name):
        
        # openapi 사용해서 영양소 xml data 받아옴
        url = f"http://openapi.foodsafetykorea.go.kr/api/{self.nut_api_key}/I2790/xml/1/1/DESC_KOR={food_name}"
        response = requests.get(url)
        xml_data = response.content
        
        # BeautifulSoup를 사용하여 XML 데이터 파싱
        soup = BeautifulSoup(xml_data, 'xml')

        # 결과 코드와 메시지가 있는지 확인
        result_code_tag = soup.find('CODE')
        result_msg_tag = soup.find('MSG')

        # 결과 코드와 메시지가 있을 경우, 오류 여부 확인
        if result_code_tag and result_msg_tag:
            result_code = result_code_tag.text
            result_msg = result_msg_tag.text

            # 결과 코드에 따른 오류 처리
            if result_code != "INFO-000":
                return {"error": True, "code": result_code, "message": result_msg}

        # 필요한 영양소 정보 추출 및 float로 변환        
        def get_nutrient_value(tag_name):
            tag = soup.find(tag_name)
            return float(tag.text) if tag and tag.text else 0.0

        calories = get_nutrient_value('NUTR_CONT1')
        carbohydrates = get_nutrient_value('NUTR_CONT2')
        protein = get_nutrient_value('NUTR_CONT3')
        fat = get_nutrient_value('NUTR_CONT4')
        sugars = get_nutrient_value('NUTR_CONT5')
        sodium = get_nutrient_value('NUTR_CONT6')
        cholesterol = get_nutrient_value('NUTR_CONT7')
        saturated_fat = get_nutrient_value('NUTR_CONT8')
        trans_fat = get_nutrient_value('NUTR_CONT9')        

        # 데이터를 사전 형태로 저장, 키를 한글로 변경
        nutritional_info = {
            '칼로리': calories,
            '탄수화물': carbohydrates,
            '단백질': protein,
            '지방': fat,
            '당류': sugars,
            '나트륨': sodium,
            '콜레스테롤': cholesterol,
            '포화지방': saturated_fat,
            '트랜스지방': trans_fat
        }

        return {"error": False, "nutritional_info": nutritional_info}
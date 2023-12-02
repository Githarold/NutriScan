import os, requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv

class GetInfo:
    
    def __init__(self):
        
        # API KEY 가져옴
        load_dotenv(find_dotenv())
        self.nut_api_key = os.getenv('NUT_TOKEN')
        self.client = OpenAI(api_key=os.environ['GPT_TOKEN'])
        print(self.client)
        
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 35
    
    # input : 부족 영양소 정보 딕셔너리 | output : 추천 음식 문자열
    def get_info_gpt(self, deficient_nutrients):
        # 부족한 영양소와 양을 문장으로 변환
        nutrient_info = ", ".join([f"{nutrient}: {amount}" for nutrient, amount in deficient_nutrients.items()])
        prompt = f"다음 영양소가 부족합니다: {nutrient_info}. 이 영양소를 보충할 수 있는 요리 메뉴 하나만 알려주세요."

        # 메시지 형식으로 요청 생성
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "name":"example_user", "content": "다음 영양소가 부족합니다: calories: 100g, protein: 25g. 이 영양소를 보충할 수 있는 요리 메뉴 이름만 알려주세요."},
                {"role": "system", "name": "example_assistant", "content": "닭 가슴살 샐러드"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens
        )

        # 응답에서 텍스트 추출
        # 'message' 객체가 아닌 'text' 속성을 사용하여 텍스트 내용을 추출
        recommended_food = response.choices[0].message.content.strip()  # 'message.content' 속성 사용

        return recommended_food
    
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
    
if __name__ == "__main__":
    # GetInfo 클래스 인스턴스 생성
    info_getter = GetInfo()

    # # 테스트하고 싶은 음식 이름
    # food_name = "귤"

    # # 영양소 정보 조회
    # nutritional_info = info_getter.get_info_openapi(food_name)

    # # 결과 출력
    # if nutritional_info.get('error'):
    #     print("Error:", nutritional_info.get('message'))
    # else:
    #     print("Nutritional Information for", food_name, ":")
    #     for nutrient, value in nutritional_info.get('nutritional_info').items():
    #         print(f"{nutrient}: {value}")
    
    nutrient_deficiencies = {
        "calories": "100g",
        "protein": "25g"
    }  # 부족한 영양소와 양
    
    recommendation = info_getter.get_info_gpt(nutrient_deficiencies)
    print(recommendation)
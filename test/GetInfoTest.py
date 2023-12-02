import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from GetFoodNutrient import Parser
from RecommandFood import Recommander

nut_parser = Parser()
food_recommander = Recommander()

# 테스트하고 싶은 음식 이름
food_name = "귤"

# 영양소 정보 조회
nutritional_info = nut_parser.get_info_openapi(food_name)

# 결과 출력
if nutritional_info.get('error'):
    print("Error:", nutritional_info.get('message'))
else:
    print("Nutritional Information for", food_name, ":")
    for nutrient, value in nutritional_info.get('nutritional_info').items():
        print(f"{nutrient}: {value}")

nutrient_deficiencies = {
    "calories": "100g",
    "protein": "25g"
}  # 부족한 영양소와 양

recommendation = food_recommander.get_info_gpt(nutrient_deficiencies)
print(recommendation)
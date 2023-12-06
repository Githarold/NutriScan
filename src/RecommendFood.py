import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


class Recommender:
    def __init__(self, user_credentials, user_id):
        # API KEY 가져옴
        load_dotenv(find_dotenv())
        self.client = OpenAI(api_key=os.environ["GPT_TOKEN"])

        self.model = "gpt-3.5-turbo"
        self.max_tokens = 35

        self.allergies = user_credentials[user_id]["details"]["allergies"]

    # input : 부족 영양소 정보 딕셔너리 | output : 추천 음식 문자열
    def get_info_gpt(self, deficient_nutrients):
        # 부족한 영양소와 양을 문장으로 변환
        nutrient_info = ", ".join(
            [
                f"{nutrient}: {amount}"
                for nutrient, amount in deficient_nutrients.items()
            ]
        )
        prompt = f"다음 영양소가 부족합니다: {nutrient_info}. {self.allergies}에 대한 알레르기를 가지고 있을 때, 이 영양소를 보충할 수 있는 요리 메뉴 하나만 알려주세요."

        # 메시지 형식으로 요청 생성
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "name": "example_user",
                    "content": "다음 영양소가 부족합니다: calories: 100g, protein: 25g. 견과류에 대한 알레르기를 가지고 있을 때, 이 영양소를 보충할 수 있는 요리 메뉴 이름만 알려주세요.",
                },
                {"role": "system", "name": "example_assistant", "content": "닭 가슴살 샐러드"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
        )

        # 응답에서 텍스트 추출
        # 'message' 객체가 아닌 'text' 속성을 사용하여 텍스트 내용을 추출
        recommended_food = response.choices[
            0
        ].message.content.strip()  # 'message.content' 속성 사용

        return recommended_food

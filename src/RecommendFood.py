import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


class Recommender:
    def __init__(self, user_credentials, user_id):
        # Load the API key
        load_dotenv(find_dotenv())
        self.client = OpenAI(api_key=os.environ["GPT_TOKEN"])

        self.model = "gpt-3.5-turbo"
        self.max_tokens = 35

        # Store user allergies information
        self.allergies = user_credentials[user_id]["details"]["allergies"]

    def get_info_gpt(self, deficient_nutrients):
        # Convert the deficient nutrients information into a string
        nutrient_info = ", ".join(
            [
                f"{nutrient}: {amount}"
                for nutrient, amount in deficient_nutrients.items()
            ]
        )
        # Create a prompt for the GPT model using the nutrient info and user's allergies
        prompt = f"다음 영양소가 부족합니다: {nutrient_info}. {self.allergies}에 대한 알레르기를 가지고 있을 때, 이 영양소를 보충할 수 있는 요리 메뉴 하나만 알려주세요."

        # Create a request in message format for the GPT model
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

        # Extract the recommended food text from the response
        recommended_food = response.choices[0].message.content.strip()

        return recommended_food

from dotenv_vault import load_dotenv
from groq import Groq
import instructor
from pydantic import BaseModel

load_dotenv()

client = Groq();
client = instructor.from_groq(client)

class RestaurantInfo(BaseModel):
    name: str
    description: str
    menu_items: list[str]

class TourInfo(BaseModel):
    title: str
    introduction: str
    conclusion: str
    restaurants: list[RestaurantInfo]

system_message = '''
You are an avid reader and a foodie. You've always dreamed of going on imagined food tours with your favorite storybook characters.
Your job is to plan a food tour for a literary character and decide what type of food you will eat.

You'll be given a literary character and a type of cuisine. You need to come up with three restaurants you'd like to visit on your food tour.
You should introduce the tour with a few sentences that weaves the character's story and restaurants together. 
After you list the restaurants, you should include a concluding paragraph that highlights what makes this tour special for the character.

For each restaurant you should include the restaurant Name, a description or the restaurant's special features that will appeal to the character and a few unique menu items that the character might enjoy.

If you're not familiar with the character or cuisine, feel free to make up the details. The goal is to create a fun and engaging food tour experience.
'''

def get_food_tour(character, cuisine):
    print(f'Requesting {cuisine} food tour for {character}')
    ai_result = None
    try:
        ai_result = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f'You are planning a food tour for literary character {character} and want to eat {cuisine} food.'},
            ],
            temperature=1.0,
            response_model=TourInfo
        )

        print('AI completion:', ai_result)
    except Exception as e:
        print('Error requesting AI completion:', e)

    return ai_result

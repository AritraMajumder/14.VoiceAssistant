import json
import requests
from keys import *


def tasker(body):
    headers = {"Authorization": "Bearer "+eden_key}
    #text1 = "to make a snowman first roll a few balls of snow but dont use yellow snow. then stack the balls on top of each other the smallest one on top the biggest on the ground. put a carrot in the top most sphere but dont let your pet rabbit starve. optionally put a hat to make the snowman a real gentleman."
    #text2 = "add 2 and 2. subtract 3 and 3"
    #body = text1+text2
    url ="https://api.edenai.run/v2/text/question_answer"
    payload={"providers": "openai", "texts": [body],'question':"what are the tasks given here?", "examples_context":"In 2017, U.S. life expectancy was 78.6 years.", "examples":[["What is human life expectancy in the United States?", "78 years."],]}
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['answers']


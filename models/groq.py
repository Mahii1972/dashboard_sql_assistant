import os
from groq import Groq
import yaml

# Load the prompt from db_schema.yaml
with open('prompts/db_schema.yaml', 'r') as file:
    db_schema = yaml.safe_load(file)
system_prompt = db_schema['template']

def get_chat_completion(user_context: str):
    client = Groq(
        # This is the default and can be omitted
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": system_prompt + user_context,
            }
        ],
        model="gemma2-9b-it"
    )

    return chat_completion.choices[0].message.content

# Example usage
user_context = "Explain the importance of fast language models"
print(get_chat_completion(user_context))
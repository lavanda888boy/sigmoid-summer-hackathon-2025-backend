import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_repository_topics(repo_description):
  response = client.chat.completions.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": "I am going to give you a repository description, and you will return the most relevant topics for it: frontend, backend, game_dev, mobile or docs. You can mention several topics (not all of them at once), nothing else is allowed."},
      {"role": "user", "content": "The repository descriptions is: " + repo_description}
    ]
  )

  return response.choices[0].message.content.split(", ")
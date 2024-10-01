from typing import List
import click
from openai import OpenAI
from pydantic import BaseModel


@click.command()
@click.argument('transcript', type=click.File('r'))
def improve_transcribe(transcript):
  client = OpenAI()

  class Conversations(BaseModel):
    m: List[str]


  response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You will be helping me to create a dataset for a fine-tuned model."},
      # {"role": "user", "content": "I am building an AI conversation app that will help the user to learn conversation with elementary Japanese. The user typically pursuing JLPT N5. The app will sometime initiate the conversation, or the user will be the one. The fine-tuned model should be able to bring an engaging conversation within the user's language capability.\nHelp me to create the data for fine-tuning the model. The data that I got do not have information of who is talking. Sometime, the sentence is separated in two or more rows. If possible, you need to improve or correct the conversation as well."},
      {"role": "user", "content": "I have data of two people talking to each other, but we don't know which one say what. Sometime, the sentence is separated in two or more rows. Please improve the conversation and puntucation. Explore the data and create a dataset for fine-tuning the model. Conversation need to follow JLPT N5 level."},
      {"role": "user", "content": f"\n{transcript.read()}"}
    ],
    response_format=Conversations
  )

  print(response.choices[0].message.content)

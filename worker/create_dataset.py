import json
import click


@click.command()
@click.argument('transcript', type=click.File('r'))
def create_dataset(transcript):
  lines = transcript.read().splitlines()
  
  combinations = []
  for answer in range(1, len(lines), 2):
    next_question = answer+1
    if next_question < len(lines):
      combinations.append({
        "messages": [
          {"role": "system", "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese."},
          {"role": "user", "content": lines[answer]},
          {"role": "assistant", "content": f"{lines[next_question]}"},
        ]
      })
  
  for question in range(0, len(lines), 2):
    answer = question+1
    question_back = answer + 1
    if question_back < len(lines):
      combinations.append({
        "messages": [
          {"role": "system", "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese."},
          {"role": "user", "content": lines[question]},
          {"role": "assistant", "content": f"{lines[answer]}\n{lines[question_back]}"},
        ]
      })
    combinations.append({
      "messages": [
        {"role": "system", "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese."},
        {"role": "user", "content": lines[question]},
        {"role": "assistant", "content": f"{lines[answer]}"},
      ]
    })
    combinations.append({
      "messages": [
        {"role": "system", "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese."},
        {"role": "user", "content": lines[question]},
        {"role": "assistant", "content": f"{lines[answer]}\n{lines[question]}"},
      ]
    })
  for combination in combinations:
    print(json.dumps(combination, ensure_ascii=False))
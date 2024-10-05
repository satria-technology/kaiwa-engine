import json


def create_dataset(transcripts: list[str]):
    combinations = []
    for answer in range(1, len(transcripts), 2):
        next_question = answer + 1
        if next_question < len(transcripts):
            combinations.append(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese.",
                        },
                        {"role": "user", "content": transcripts[answer]},
                        {
                            "role": "assistant",
                            "content": f"{transcripts[next_question]}",
                        },
                    ]
                }
            )

    for question in range(0, len(transcripts), 2):
        answer = question + 1
        question_back = answer + 1
        if question_back < len(transcripts):
            combinations.append(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese.",
                        },
                        {"role": "user", "content": transcripts[question]},
                        {
                            "role": "assistant",
                            "content": f"{transcripts[answer]}\n{transcripts[question_back]}",
                        },
                    ]
                }
            )
        combinations.append(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese.",
                    },
                    {"role": "user", "content": transcripts[question]},
                    {"role": "assistant", "content": f"{transcripts[answer]}"},
                ]
            }
        )
        combinations.append(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are learning buddy for JLPT N5 student. You are helping the student to learn conversation in Japanese.",
                    },
                    {"role": "user", "content": transcripts[question]},
                    {
                        "role": "assistant",
                        "content": f"{transcripts[answer]}\n{transcripts[question]}",
                    },
                ]
            }
        )
    return combinations

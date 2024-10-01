import click
from dotenv import load_dotenv

load_dotenv()


from worker.create_dataset import create_dataset
from worker.improve_transcribe import improve_transcribe
from worker.transcribe_youtube import transcribe_youtube

@click.group()
def cli():
  pass

cli.add_command(transcribe_youtube)
cli.add_command(improve_transcribe)
cli.add_command(create_dataset)

if __name__ == "__main__":
  cli()
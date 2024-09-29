import click

from worker.transcribe_youtube import transcribe_youtube

@click.group()
def cli():
  pass

cli.add_command(transcribe_youtube)

if __name__ == "__main__":
  cli()
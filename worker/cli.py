import click
from worker.transcribe_youtube import transcribe_youtube
from worker.improve_transcribe import improve_transcribe
from worker.create_dataset import create_dataset

@click.group()
def cli():
  pass

@click.command()
@click.option('--urls', multiple=True, prompt='YouTube URL', help='URL of the YouTube video to transcribe')
def transcribe_youtube_command(urls: tuple):
  transcribe_youtube(urls)

@click.command()
@click.argument('transcript', type=click.File('r'))
def improve_transcribe_command(transcript):
  improve_transcribe(transcript.read())

@click.command()
@click.argument('transcript', type=click.File('r'))
def create_dataset_command(transcript):
  transcripts = transcript.read().split('\n')
  create_dataset(transcripts)

cli.add_command(transcribe_youtube_command)
cli.add_command(improve_transcribe_command)
cli.add_command(create_dataset_command)

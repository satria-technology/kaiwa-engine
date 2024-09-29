import click
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


@click.command()
@click.option('--urls', multiple=True, prompt='YouTube URL', help='URL of the YouTube video to transcribe')
def transcribe_youtube(urls: tuple):
    for url in urls:
        # Extract video ID from URL
        # Parse the URL and extract the video ID from the query parameters
        query_params = parse_qs(urlparse(url).query)
        video_id = query_params.get('v', [None])[0]

        if not video_id:
            print(f"Could not extract video ID from URL: {url}")
            continue

        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja'])

        # Combine transcript segments into a single string
        full_transcript = '\n'.join([segment['text'] for segment in transcript])

        print(f"Transcription for {url}:\n{full_transcript}\n\n")



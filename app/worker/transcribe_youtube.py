from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def transcribe_youtube(urls: tuple):
  results = []
  for url in urls:
    # Extract video ID from URL
    # Parse the URL and extract the video ID from the query parameters
    query_params = parse_qs(urlparse(url).query)
    video_id = query_params.get('v', [None])[0]

    if not video_id:
      results.append(f"Could not extract video ID from URL: {url}")
      continue

    # Fetch the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja'])

    # Combine transcript segments into a single string
    for segment in transcript:
      results.append(segment['text'])

import os
from googleapiclient.discovery import build

def search_youtube_videos(query: str, max_results: int = 3):
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("WARNING: YOUTUBE_API_KEY not found.")
        return []

    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        
        request = youtube.search().list(
            part="snippet",
            maxResults=max_results,
            q=query,
            type="video"
        )
        response = request.execute()
        
        videos = []
        for item in response.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "channel": item["snippet"]["channelTitle"]
            })
        return videos
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

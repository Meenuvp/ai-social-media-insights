from googleapiclient.discovery import build

YOUTUBE_API_KEY = "AIzaSyB28vcIdF68o1JtrRbGckdGwsmEtbcWiRY"

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def get_channel_id(input_value):
    """
    Converts username / handle / channelId into valid channelId
    """
    # If already channel ID
    if input_value.startswith("UC"):
        return input_value

    # Try resolving username / handle
    request = youtube.search().list(
        part="snippet",
        q=input_value,
        type="channel",
        maxResults=1
    )
    response = request.execute()

    if response["items"]:
        return response["items"][0]["snippet"]["channelId"]

    return None


def fetch_youtube_comments(input_value, max_results=20):
    channel_id = get_channel_id(input_value)

    if not channel_id:
        return []

    # Get recent videos
    search_request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=5,
        order="date"
    )
    search_response = search_request.execute()

    comments = []

    for item in search_response["items"]:
        video_id = item["id"].get("videoId")
        if not video_id:
            continue

        comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results
        )
        comment_response = comment_request.execute()

        for c in comment_response["items"]:
            text = c["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

    return comments

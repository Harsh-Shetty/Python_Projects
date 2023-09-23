"""
Code for calculating PLAYLIST DURATION & VIEWS on VIDEOS from that PLAYLIST.
Run in virtual environment. Create new API_KEY here: https://console.developers.google.com/
Refer this video from 1:41 - https://youtu.be/th5_9woFJmk

Refer this Document: (Building and calling a service)
https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md

build(serviceName, version, http=None, discoveryServiceUrl=DISCOVERY_URI,
        developerKey=None, model=None, requestBuilder=HttpRequest, 
        credentials=None, cache_discovery=True, cache=None, client_options=None, 
        adc_cert_path=None, adc_key_path=None, num_retries=1) 
https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build

Instance Methods: https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html
like channels() : https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.channels.html
Also refer this for parameters for channels().list(): https://developers.google.com/youtube/v3/docs/channels/list

viewCount is fetched using YT statistics dictionary.
Reference: https://developers.google.com/youtube/v3/docs/videos#resource-representation
"""

import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = os.environ.get("API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)

# d means Digits, + means one or more.
# (\d+) means grab one or more digits before H
hours_pattern = re.compile(r"(\d+)H")
minutes_pattern = re.compile(r"(\d+)M")
seconds_pattern = re.compile(r"(\d+)S")

totalSeconds = 0

playlist_Id = "PLkN0ph2Bzv2NfcBdvw5JNFM1tHgcpJyMR"

# This dict will contain viewCount & dislikeCount keys for
# vals of video links
videos = []

nextPageToken = None

print("Fetching data from YouTube servers. Please wait...")
print()

while True:
    """
    Request Playlist with playlistId
    """
    pl_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_Id, #must be playlistId as mentioned in the documentation
        maxResults=50,  # 50 resuts at once per request. This is recommeded as
        # doesn't clog up the server with multiple single result requests
        pageToken=nextPageToken,  # 50 requests per page. Then move to
        # next page
    )

    pl_response = pl_request.execute()

    """
    Request VIDEOS from the previously fetched PLAYLIST in order to get durtion 
    key in contentDetails & viewCount in statistics.
    """
    # fetches video id
    vid_ids = []
    for item in pl_response["items"]:
        vid_ids.append(item["contentDetails"]["videoId"])

    vid_request = youtube.videos().list(
        part=["statistics", "contentDetails"],
        id=",".join(vid_ids),  # getting comma separated vals of list of vid_ids
    )

    vid_response = vid_request.execute()

    """
    Get DURATION of each video & then calculate total time (i.e time to watch
    the entire PLAYLIST)
    """

    for item in vid_response["items"]:
        # fetching duration key from list of contentDetails
        duration = item["contentDetails"]["duration"]

        # fetching viewCount & dislikeCount keys from list of statistics
        vid_views = item["statistics"]["viewCount"]

        # creating link to each video in the playlist
        vid_id = item["id"]
        yt_link = f"https://youtu.be/{vid_id}"

        # Empty dictionary created in line 40
        videos.append({"Views": int(vid_views), "url": yt_link})

        # this gives result like: None <re.Match object; span=(2, 5),
        # match='23M'> <re.Match object; span=(5, 7), match='1S'>.
        # None if one of the val is 0 (here it is hours)
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        # this will make the result like 23 (for mins)
        # if the val is None (i.e 0) then print 0 with if...else statement
        # x.group gives a str so we convert it into integer
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        # converts into seconds
        video_seconds = timedelta(
            hours=hours, minutes=minutes, seconds=seconds
        ).total_seconds()  # In-built func. Not related totalSeconds in line 34.
        # Caclulates total seconds for each video, not the summation of the entire playlist

        totalSeconds += video_seconds  # Gives total seconds of the entire PLAYLIST

    # pl_response tries to get the next page. If it fails to make more requests
    # to print on the next page then it sets nextPageToken to NONE
    nextPageToken = pl_response.get("nextPageToken")
    # if nextPageToken is NONE then break the loop
    if not nextPageToken:
        break

totalSeconds = int(totalSeconds)

# returns a tuple of division of totalSeconds by 60. Minutes will be
# quotient & remainder will be seconds
minutes, seconds = divmod(totalSeconds, 60)

# sorts the videos according to descending order of VIEWS.
videos.sort(key=lambda vid: vid["Views"], reverse=True)

# for hours
hours, minutes = divmod(minutes, 60)
print(f"Total Playlist duration: {hours}H {minutes}M {seconds}s")
print()

for video in videos:
    print(video["url"], video["Views"])

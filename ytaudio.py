from __future__ import unicode_literals
import youtube_dl
import os

ydl_opts = {
    'outtmpl': 'downloaded_music/%(title)s-%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def download(song_url):
    try:
        os.makedirs("downloaded_music")
    except FileExistsError:
        # directory already exists
        pass
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_url])

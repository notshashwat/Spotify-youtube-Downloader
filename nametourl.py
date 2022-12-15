# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
import secretkeys

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"


api_key = secretkeys.google_api_key
youtube = build(api_service_name, api_version, developerKey=api_key)

def query(q):
    '''
    Return the youtube url of the first search result from query q
    '''
    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q=q 
    )
    response = request.execute()
    url =[]
    video_url = 'https://www.youtube.com/watch?v=' + str(response['items'][0]['id']['videoId'])
    return (video_url)



def main():
    query("fix you- coldplay")
  
if __name__ == "__main__":
    main()
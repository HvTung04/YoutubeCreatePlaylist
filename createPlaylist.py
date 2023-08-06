import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # No valid credentials -> login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: # Create first time
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())
    
    try:
        service = build('youtube', 'v3', credentials=creds)

        # Create playlist
        playlist_title = "My test playlist"
        privacy_status = "private"
        response = service.playlists().insert(
            part='snippet,status',
            body= {
                'snippet': {
                    'title': playlist_title,
                    'description': 'My testing playlist'
                },
                'status': {
                    'privacyStatus': privacy_status,
                },
            }
        ).execute()
        playlist_id = response.get('id')
        print(f"Playlist '{playlist_title}' created with ID: {playlist_id}")
    except HttpError as error:
        print("An error occured", error)


if __name__ == "__main__":
    main()
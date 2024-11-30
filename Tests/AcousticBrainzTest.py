import requests

# track_name = "Cadillac"
# artist_name = "Black Honey"
track_name = "Let It Be"
artist_name = "The Beatles"
# track_name = "Get It ON"
# artist_name = "T.Rex"
# track_name = "Starman"
# artist_name = "David Bowie"

MBIDquery = f"https://musicbrainz.org/ws/2/recording/?query=track:{track_name} AND artist:{artist_name}&fmt=json"

response = requests.get(MBIDquery, headers={"User-Agent": "IOT_Music/1.0 (l.westerburgburr@gmail.com)"})

if response.status_code == 200:
    data = response.json()
    if data.get('recordings'):
        recording = data.get('recordings')
        #print(recording)
        title = recording[1]['title']
        MBID = recording[1]['id']
        print(f"Track: {title}, MBID: {MBID}")
        # for recording in data['recordings']:
        #     print(f"Track: {recording['title']}, MBID: {recording['id']}")
    else:
        print("No recordings found.")
else:
    print(f"Error {response.status_code}: {response.text}")

#MBID = "b1a9c0e9-d987-4042-ae91-78d6a3267d69"

infoquery = f"https://acousticbrainz.org/{MBID}/high-level"

response = requests.get(infoquery)
print(response.headers)

if response.status_code == 200:
    data = response.json()  
    #print("High-level data:", data)
    danceability = data['highlevel']['danceability']['all']['danceable']
    happiness = data['highlevel']['mood_happy']['all']['happy']
    partyness = data['highlevel']['mood_party']['all']['party']
    relaxed = data['highlevel']['mood_relaxed']['all']
    print(f"Danceability: {danceability}")
    print(f"Happiness: {happiness}")
    print(f"Partyness: {partyness}")
    print(f"Relaxed: {relaxed}")

else:
    print(f"Error: {response.status_code}: {response.text}")



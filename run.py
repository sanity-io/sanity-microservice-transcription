import os
import json
import assemblyai
import requests
from sanic import Sanic
from sanic import response
import aiohttp
app = Sanic(__name__)
print(os.environ)
# GET ENV SECRETS
ASSEMBLY_TOKEN = os.environ.get('ASSEMBLY_TOKEN')
PROJECT_ID = os.environ.get('PROJECT_ID')
DATASET = os.environ.get('DATASET')
SANITY_TOKEN = os.environ.get('SANITY_TOKEN')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

# SET UP API CONFIG
mutations_api = "https://{}.api.sanity.io/v1/data/mutate/{}?returnIds=true&visibility=async".format(PROJECT_ID, DATASET)
auth_header = { "Authorization": "Bearer {}".format(SANITY_TOKEN) }

def check_env():
    return (
        ASSEMBLY_TOKEN is not None or
        PROJECT_ID is not None or
        DATASET is not None or
        SANITY_TOKEN is not None
    )


@app.get('/')
async def hello_world(request):
    return response.html("A transcription service for <a href='https://samity.io'>sanity.io</a> lives here.")

@app.post("/")
async def webhook_endpoint(request):
    try:
        content = request.json
        print(content['ids'])
        if (content['ids']):
            for file in content['ids']['created']:
                transcribe(file)
        return response.json(
            {"message": "ok"},
            status=200
        )
    except Exception as e:
        print(e)
        return response.json(
            {"message": "error"},
            status=500
        )

def transcribe(file):
    prepareFile = file.split("-")
    if (prepareFile[2] in ['mp3', 'wav', 'm4a']):
        file_url = "https://cdn.sanity.io/files/{}/{}/{}.{}".format(PROJECT_ID, DATASET, prepareFile[1], prepareFile[2])
        aai = assemblyai.Client(token=ASSEMBLY_TOKEN)
        transcript = aai.transcribe(audio_url=file_url)

        while transcript.status != 'completed':
            print(transcript.status)
            transcript = transcript.get()

        text = transcript.text
        print(text)
        mutations = {
            "mutations": [{
                "patch": {
                    "id": file,
                    "set": {
                        "transcription": {
                            "text": text,
                            "service": "assemblyai"
                        }
                        }
                    }
                }]
            }

        print("Sending transript of {} to Sanity".format(file))
        r = requests.post(mutations_api, data=json.dumps(mutations), headers=auth_header)
        if (r.status_code == 200 and SLACK_WEBHOOK_URL):
            payload = { "text": "File {} was transcribed successfully".format(file) }
            requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
        else:
            payload = { "text": "An error happened when transcribing {}: {}".format(file, r.message) }
            requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))


if __name__ == '__main__' and check_env():
    app.run(host="0.0.0.0", port=8006)
else:
    print('Check if environment variable is missing')
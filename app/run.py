import os
import json
import assemblyai
import requests
from flask import Flask, request, jsonify
app = Flask(__name__)

ASSEMBLY_TOKEN = os.environ.get('ASSEMBLY_TOKEN')
PROJECT_ID = os.environ.get('PROJECT_ID')
DATASET = os.environ.get('DATASET')

mutations_api = "https://{}.api.sanity.io/v1/data/mutate/{}?returnIds=true&visibility=async".format(PROJECT_ID, DATASET)
auth_header = { "Authorization": "Bearer {}".format(SANITY_TOKEN) }

@app.route("/", methods=['GET', 'POST'])
def hello():
    content = request.get_json()
    print(content['ids'])
    if (content['ids']):
        for file in content['ids']['created']:
            transcribe(file)
        return jsonify(content)

def transcribe(file):
    prepareFile = file.split("-")
    if (prepareFile[2] in ['mp3', 'wav', 'm4a']):
        file_url = "https://cdn.sanity.io/files/{}/{}/".format(PROJECT_ID, DATASET, prepareFile[1], prepareFile[2])
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
                        "transcript": text
                        }
                    }
                }]
            }

        print("Sending transript to {}".format(mutations_api))
        r = requests.post(mutations_api, data=json.dumps(mutations), headers=auth_header)
        print(r.status_code)
        print(r.reason)
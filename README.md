# 🗣📝 Microservice for transcribing audio files uploaded to [sanity.io](https://sanity.io)

[![Demo on youtube](https://cdn.sanity.io/images/3do82whm/production/e87421b91f2ed0f20ee91bde7d79ebb355157a98-2560x1440.png)](https://www.youtube.com/watch?v=8Kl1ySmXGO4)

This transcription microservice is an example for how to leverage [webhooks in Sanity](https://www.sanity.io/docs/webhooks). It takes uploaded audio files, and requests a transcription from [assemblyai](https://assemblyai.com/), and writes that on the file asset metadata. Obviously, it works best on spoken tracks (such as podcasts) and your machine learning fueled milage may vary (it's always fun though!).

The Python app uses [Sanic](http://sanic.readthedocs.io/), which is a [Flask](http://flask.pocoo.org/)-like server with support for Python 3.5’s async capabilities, and is inspired by [this blog on how to write such a microservice](https://simonwillison.net/2017/Oct/14/async-python-sanic-now/).


## Deploying on ▲ `now`
[![Deploy to now](https://deploy.now.sh/static/button.svg)](https://deploy.now.sh/?repo=https://github.com/sanity-io/sanity-microservice-transcription?env=ASSEMBLY_TOKEN&env=PROJECT_ID&env=DATASET&env=SLACK_WEBHOOK_URL&env=SANITY_TOKEN)

(remember to `☑️  Build using Docker`)

Or clone this repo and follow these instructions:

1. Register an account at [assemblyai.com](https://assemblyai.com/) to get an API token
2. Generate a Sanity token with write permissions at [manage.sanity.io](https://manage.sanity.io)
3. Find your project ID and dataset name (`$ sanity projects list`)
4. Add an optional Slack Webhook URL if you want the service to notify a slack channel of ready transcriptions.
5. Run `now` and paste the variables when prompted
6. The `now` app URL should be copied automatically to your clipboard. You can now run `sanity hook create` in your Sanity project folder and paste in the URL when prompted for  it.
7. That's it!
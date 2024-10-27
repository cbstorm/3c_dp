from label_studio_sdk.client import LabelStudio

LABEL_STUDIO_URL = 'http://localhost:8888'
LABEL_STUDIO_APIKEY = '43cf784d62b4bda29f0a8fe0032ddb0f3784e8c3'

client = LabelStudio(
    base_url=LABEL_STUDIO_URL,
    api_key=LABEL_STUDIO_APIKEY,
)

# 1024x1024 0.02$
# 512x512 0.018$
# 256x256 0.016$

import openai
import config

openai.api_key = config.api_key

try:
    response = openai.Image.create(
      prompt="a white siamese cat",
      n=1,
      size="256x256"
    )
    image_url = response['data'][0]['url']
    print(image_url)
except openai.error.OpenAIError as e:
    print(e.http_status)
    print(e.error)

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("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"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hi"}]
)

print(response.choices[0].message.content)

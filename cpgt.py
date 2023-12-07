import openai 

client = openai.OpenAI(api_key = "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")

def sendToGPT(data):

  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": data}
  ]
  )    
  
  return completion.choices[0].message.content



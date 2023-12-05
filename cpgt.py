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



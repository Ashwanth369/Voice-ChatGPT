import openai 

client = openai.OpenAI(api_key = "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")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
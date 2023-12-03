from openai import OpenAI
from emigration_bot.api_keys import GPT_KEY

client = OpenAI(api_key=GPT_KEY)
counter = 0
def get_response(prompts):
  system_promt, user_promt = prompts
  print(system_promt)
  print(user_promt)
  try:
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": system_promt},
        {"role": "user", "content": user_promt}
      ],
    max_tokens = 500
    )

    return completion.choices[0].message
  except Exception as e:
    print(e)
    return None
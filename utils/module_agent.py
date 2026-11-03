from openai import OpenAI

def extract_modules(text, model, api_key=None):
    prompt = f'''Identify modules and submodules and return JSON.\n{text[:12000]}'''
    client = OpenAI(api_key=api_key) if api_key else OpenAI()
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

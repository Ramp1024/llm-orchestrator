import json
from openai import OpenAI

client = OpenAI()

def generate_dsl(prompt, config, tool):

    system_prompt = tool.generate_prompt(config, prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    
    # Remove markdown code blocks if present
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    content = content.strip()
    
    print(f"\nLLM Response:\n{content}")
    
    return json.loads(content)
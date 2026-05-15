import json
from openai import OpenAI
from openai import RateLimitError
from dotenv import load_dotenv

load_dotenv(override=True)

def generate_dsl(prompt, config, tool):

    system_prompt = tool.generate_prompt(config, prompt)

    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
    except RateLimitError as exc:
        raise RuntimeError(
            "OpenAI quota check failed (429 insufficient_quota). "
            "Verify that OPENAI_API_KEY in .env belongs to the same billed project/org and has available credits."
        ) from exc

    content = response.choices[0].message.content
    
    # Remove markdown code blocks if present
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    content = content.strip()
    
    print(f"\nLLM Response:\n{content}")
    
    return json.loads(content)
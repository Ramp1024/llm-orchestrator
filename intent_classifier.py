from openai import OpenAI
from openai import RateLimitError
from dotenv import load_dotenv
from tool_registry import TOOLS
import json

load_dotenv(override=True)

def classify_intent(prompt):

    tools_desc = "\n".join([
        f"{name}: {tool.description}"
        for name, tool in TOOLS.items()
    ])

    system_prompt = f"""
Available operations:
{tools_desc}

Pick the best operation.
Return JSON:
{{ "intent": "<tool_name>" }}
"""

    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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

    return json.loads(content)["intent"]
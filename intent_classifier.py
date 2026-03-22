from openai import OpenAI
from tool_registry import TOOLS
import json

client = OpenAI()

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)["intent"]
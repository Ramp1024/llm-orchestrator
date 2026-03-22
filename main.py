import json
from intent_classifier import classify_intent
from llm_service import generate_dsl
import os
from dsl_models import WorkflowDSL
from tool_registry import TOOLS
print(os.getenv("OPENAI_API_KEY"))

def load_config():
    with open("sample_config.json") as f:
        config = json.load(f)

    actions = json.loads(config["Value"])

    return config, actions


def print_actions(actions):
    print("\nExisting actions:\n")

    for action in actions:
        print(
            f'Id: {action["Id"]}, '
            f'Label: {action["Label"]}, '
            f'Type: {action["Type"]}'
        )

def load_dsl(user_prompt, actions):

    intent = classify_intent(user_prompt)

    print(f"\nClassified intent: {intent}")

    tool = TOOLS[intent]

    print(f"\nUsing tool: {tool.name} - {tool.description}")

    dsl_raw = generate_dsl(user_prompt, actions, tool)

    # Handle different response formats
    if isinstance(dsl_raw, list):
        operation_data = dsl_raw[0]
    elif isinstance(dsl_raw, dict):
        if "operations" in dsl_raw:
            operation_data = dsl_raw["operations"][0]
        else:
            operation_data = dsl_raw
    else:
        raise ValueError(f"Unexpected DSL format: {type(dsl_raw)}")

    operation = tool.schema(**operation_data)

    actions = tool.execute(actions, operation)
    
    print("\nGenerated DSL:")
    print(json.dumps(dsl_raw, indent=2))

    return actions

def main():

    config, actions = load_config()

    user_prompt = input("Enter instruction:\n")

    updated_actions = load_dsl(user_prompt, actions)

    payload = build_final_payload(config, updated_actions)

    print("\nFinal API Payload:\n")

    print(json.dumps(payload, indent=2))

def build_final_payload(config, updated_actions):

    payload = config.copy()

    payload["Value"] = json.dumps(updated_actions)

    return payload


if __name__ == "__main__":
    main()
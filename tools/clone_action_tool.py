from dsl_models import CloneAction
from action_utils import apply_clone_operation
from tools.base_tool import BaseTool

class CloneActionTool(BaseTool):
    name = "clone_action"
    description = "Create new actions from an existing one"
    schema = CloneAction

    def generate_prompt(self, config, user_prompt):

        schema_text = self.get_schema_text()

        return f"""
            You are generating DSL for the tool: {self.name}

            Description:
            {self.description}

            User request:
            {user_prompt}

            Existing configuration:
            {config}

            You MUST return JSON with the following fields:

            {schema_text}

            Rules:
            - Do NOT invent new fields
            - Do NOT return full action objects
            - Only return fields defined above
            - Ensure all required fields are present
            - "type" must always be "{self.name}"

            Example:

            {{
            "type": "clone_action",
            "sourceAction": "SendforReview",
            "newLabels": [
                "Send for Internal Review",
                "Send for External Review"
            ]
            }}

            Return ONLY JSON.
            """

    def execute(self, actions, operation):
        return apply_clone_operation(actions, operation)
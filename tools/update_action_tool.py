from dsl_models import UpdateActionProperty
from tools.base_tool import BaseTool

class UpdateActionTool(BaseTool):
    name = "update_action_property"
    description = "Update properties of an existing action"
    schema = UpdateActionProperty

    def generate_prompt(self, config):
        return f"""
Generate update_action_property DSL.

Config:
{config}

Return JSON only.
"""

    def execute(self, actions, operation):
        return apply_update_operation(actions, operation)
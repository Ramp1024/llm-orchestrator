from tools.clone_action_tool import CloneActionTool
from tools.update_action_tool import UpdateActionTool

TOOLS = {}

def register_tools():
    for tool in [CloneActionTool(), UpdateActionTool()]:
        TOOLS[tool.name] = tool

register_tools()
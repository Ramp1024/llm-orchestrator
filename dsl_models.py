from pydantic import BaseModel
from typing import List, Literal, Union


class CloneAction(BaseModel):
    type: Literal["clone_action"]
    sourceAction: str
    newLabels: List[str]


class UpdateActionProperty(BaseModel):
    type: Literal["update_action_property"]
    actionId: str
    property: str
    value: str

Operation = Union[CloneAction, UpdateActionProperty]

class WorkflowDSL(BaseModel):
    intentType: str
    activityName: str
    operations: List[Operation]
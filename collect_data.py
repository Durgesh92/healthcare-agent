import json
import os
from typing import Optional, Type

from pydantic.v1 import BaseModel, Field

from vocode.streaming.action.abstract_factory import AbstractActionFactory
from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import ActionConfig as VocodeActionConfig
from vocode.streaming.models.actions import ActionInput, ActionOutput, PhraseBasedActionTrigger, PhraseBasedActionTriggerConfig, PhraseTrigger

    
_DATA_ACTION_DESCRIPTION = """
Records health data collected from the patient.
The data is stored in a dictionary and then it is saved as a JSON file.
The dictionary is then returned by the action output.
"""


class CollectDataParameters(BaseModel):
    patient_name: str = Field(..., description="The patient's name.")
    dob: str = Field(..., description="The patient's date of birth.")
    insurance_name: str = Field(..., description="The patient's insurance provider's name.")
    insurance_id: str = Field(..., description="The patient's insurance ID.")
    referral: bool = Field(..., description="Whether or not the patient has a referral.")
    refferal_physician: str = Field(..., description="The name of the physician the patient was referred to.")
    reason: str = Field(..., description="The patient's chief medical complaint/reason they are calling.")
    address: str = Field(..., description="The patient's address.")
    phone: str = Field(..., description="The patient's phone number.")
    email: str = Field(..., description="The patient's email address.")
    booked_dr: str = Field(..., description="The name of the doctor the patient is booked for.")
    booked_date: str = Field(..., description="The date of the appointment the patient is booked for.")
    


class CollectDataResponse(BaseModel):
    call_data: dict


class CollectDataActionConfig(VocodeActionConfig, type="action_collect_data"):
    # action_trigger = PhraseBasedActionTrigger(
    #     type = "action_trigger_phrase_based",
    #     config = PhraseBasedActionTriggerConfig(
    #         phrase_triggers = [
    #             PhraseTrigger(
    #                 phrase="Thank you for your time we will get back to you shortly regarding your appointment",
    #                 conditions=["phrase_condition_type_contains"]
    #             ),
    #         ]
    #     )
    # )  # type: ignore
    pass

class CollectData(
        BaseAction[
            CollectDataActionConfig,
            CollectDataParameters,
            CollectDataResponse,
        ]
    ):
    description: str = _DATA_ACTION_DESCRIPTION
    parameters_type: Type[CollectDataParameters] = CollectDataParameters
    response_type: Type[CollectDataResponse] = CollectDataResponse

    def __init__(
        self,
        action_config: CollectDataActionConfig,
    ):
        super().__init__(
            action_config,
            quiet=True,
            is_interruptible=True,
        )

    async def _end_of_run_hook(self) -> None:
        print("Successfully collected data!")
    
    async def run(
        self, action_input: ActionInput[CollectDataParameters]
    ) -> ActionOutput[CollectDataResponse]:
        
        call_data = {}
        # Create dict
        call_data = {
            "patient_name": action_input.params.patient_name.strip(),
            "dob": action_input.params.dob.strip(),
            "insurance_name": action_input.params.insurance_name.strip(),
            "insurance_id": action_input.params.insurance_id.strip(),
            "referral": action_input.params.referral,
            "refferal_physician": action_input.params.refferal_physician.strip(),
            "reason": action_input.params.reason.strip(),
            "address": action_input.params.address.strip(),
            "phone": action_input.params.phone.strip(),
            "email": action_input.params.email.strip(),
            "booked_dr": action_input.params.booked_dr.strip(),
            "booked_date": action_input.params.booked_date.strip()
        }

        print(call_data)

        # data_path = "/mnt/c/Users/serdj/healthcare-agent/data/"
        # identifier = f"{call_data['patient_name']}{call_data['dob']}".replace(" ", "_")
        # json_file = f"{data_path}{identifier}.json"
        # with open(json_file, "w") as outfile: 
        #     json.dump(call_data, outfile)


        await self._end_of_run_hook()
        return ActionOutput(
            action_type=action_input.action_config.type,
            response=CollectDataResponse(call_data=call_data),
        )
    
class DataCollectActionFactory(AbstractActionFactory):
    def create_action(self, action_config: VocodeActionConfig):
        if action_config.type == "action_collect_data":
            return CollectData(action_config)
        else:
            raise Exception("Action type not supported by Agent config.")

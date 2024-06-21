# Standard library imports
import os
import sys

from dotenv import load_dotenv

# Third-party imports
from fastapi import FastAPI
from loguru import logger
from pyngrok import ngrok

# Local application/library specific imports
from agent_factory import HealthAgentFactory
from collect_data import CollectDataActionConfig

from vocode.logging import configure_pretty_logging
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig

# if running from python, this will load the local .env
# docker-compose will load the .env file by itself
load_dotenv()

configure_pretty_logging()

app = FastAPI(docs_url=None)

config_manager = RedisConfigManager()

BASE_URL = os.getenv("BASE_URL")

if not BASE_URL:
    ngrok_auth = os.environ.get("NGROK_AUTH_TOKEN")
    if ngrok_auth is not None:
        ngrok.set_auth_token(ngrok_auth)
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 3000

    # Open a ngrok tunnel to the dev server
    BASE_URL = ngrok.connect(port).public_url.replace("https://", "")
    logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(BASE_URL, port))

if not BASE_URL:
    raise ValueError("BASE_URL must be set in environment if not using pyngrok")

init_msg = "Welcome to the Rolovic Health Clinic. Could you please provide your name and date of birth?"

PROMPT_PREAMBLE = """
I want you to act as call center agent for a health clinic being contacted by a prospective patient. 
After greeting the patient, begin to ask questions to collect the information listed below.

You must collect the following information from the patient: 
- Collect patient's name and date of birth
- Collect insurance information
    - Payer name and ID
- Ask if they have a referral, and to which physician
- Collect chief medical complaint/reason they are coming in
- Collect other demographics like address
- Collect contact information
- Offer up best available providers and times from the data in the nested list below
    - Dr. Strangelove on July 2nd at 1:00 p.m.
    - Dr. Strangelove on July 2nd at 4:00 p.m.
    - Dr. Pickle on July 3rd at 11:00 a.m.
    - Dr. Shemp on July 5th at 9:00 a.m.


Once the patient chooses which appointment they want to book, you will run the collect_data_action and say Goodbye.
"""

telephony_server = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,
    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",
            agent_config=ChatGPTAgentConfig(
                initial_message=BaseMessage(text=init_msg),
                prompt_preamble=PROMPT_PREAMBLE,
                generate_responses=True,
                actions=[
                    CollectDataActionConfig(
                        type = 'action_collect_data'
                    )
                ]
            ),
            twilio_config=TwilioConfig(
                account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                auth_token=os.environ["TWILIO_AUTH_TOKEN"],
            ),
        )
    ],
    agent_factory=HealthAgentFactory(),
)

app.include_router(telephony_server.get_router())

from dotenv import load_dotenv
import os

import vocode
from vocode.client import Vocode
from elevenlabs.client import ElevenLabs
from twilio.rest import Client

# Initialize services
load_dotenv()

vocode_client = Vocode(api_key=os.getenv('VOCODE_API_KEY'))
elevenlabs_client = ElevenLabs(os.getenv('ELEVENLABS_API_KEY'))
twilio_client = Client(os.getenv('TWILIO_ACCOUNT'), os.getenv('TWILIO_AUTH'))

# Placeholder for storing collected information
patient_info = {
    'name': None,
    'dob': None,
    'insurance': {'payer_name': None, 'payer_id': None},
    'referral': {'has_referral': None, 'physician': None},
    'chief_complaint': None,
    'address': None,
    'contact_info': None,
    'appointment': {'provider': None, 'time': None}
}

# Conversation script
def handle_call(call_sid):
    # Create a voice AI session
    session = vocode_client.create_session(call_sid)
    
    # Collect patient's name and DOB
    session.say("Hello, thank you for calling. May I have your name and date of birth?")
    patient_info['name'] = session.listen()
    patient_info['dob'] = session.listen()

    # Collect insurance information
    session.say("Can you provide your insurance payer name and ID?")
    patient_info['insurance']['payer_name'] = session.listen()
    patient_info['insurance']['payer_id'] = session.listen()

    # Ask about referral
    session.say("Do you have a referral? If yes, please provide the physician's name.")
    patient_info['referral']['has_referral'] = session.listen()
    if patient_info['referral']['has_referral'].lower() == 'yes':
        patient_info['referral']['physician'] = session.listen()

    # Collect chief complaint
    session.say("What is the reason for your visit today?")
    patient_info['chief_complaint'] = session.listen()

    # Collect address
    session.say("Can you provide your address?")
    patient_info['address'] = session.listen()

    # Collect contact information
    session.say("Lastly, can I have your contact information?")
    patient_info['contact_info'] = session.listen()

    # Offer available providers and times
    session.say("We have the following providers and times available:")
    providers = ["Dr. Smith at 10 AM", "Dr. Johnson at 2 PM", "Dr. Brown at 4 PM"]
    for provider in providers:
        session.say(provider)
    patient_info['appointment']['provider'] = session.listen()
    patient_info['appointment']['time'] = session.listen()

    # Confirm appointment
    session.say(f"Thank you. You have an appointment with {patient_info['appointment']['provider']} at {patient_info['appointment']['time']}. You will receive a confirmation text shortly.")
    
    # Send confirmation text
    twilio_client.messages.create(
        body=f"Your appointment is confirmed with {patient_info['appointment']['provider']} at {patient_info['appointment']['time']}.",
        from_= os.getenv('TWILIO_NUMBER'),  # Twilio number
        to=patient_info['contact_info']
    )

# Run the application
if __name__ == "__main__":
    vocode_client.run(handle_call)
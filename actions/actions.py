# actions/actions.py
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted, Form
from rasa_sdk.forms import FormValidationAction
from typing import Any, Text, Dict, List   # ← This line was missing!

import uuid  # <--- Add this at the top
from rasa_sdk.events import AllSlotsReset
import json


class ValidateFormGetLanguage(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_get_language"

    async def validate_selected_language(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        valid = {"English", "Amharic", "Afaan Oromoo", "ትግርኛ"}
        return {"selected_language": slot_value if slot_value in valid else None}

class ActionSubmitLanguageForm(Action):
    def name(self) -> Text:
        return "action_submit_language_form"

    async def run(self, dispatcher, tracker, domain):
        lang = tracker.get_slot("selected_language") or "English"

        greet_map = {
            "English": "utter_greet_en",
            "Amharic": "utter_greet_am",
            "Afaan Oromoo": "utter_greet_om",
            "ትግርኛ": "utter_greet_ti"
        }

        dispatcher.utter_message(response=greet_map.get(lang))

        # For Amharic, send welcome + main menu
        if lang == "Amharic":
            dispatcher.utter_message(response="utter_welcome_am")
            dispatcher.utter_message(response="utter_main_menu_am")

        return [AllSlotsReset()]





class ActionSubmitIncidentForm(Action):

    def name(self) -> Text:
        return "action_submit_incident_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. Generate a random Reference Number
        reference_number = str(uuid.uuid4())[:8].upper()

        # 2. Get the attachment input safely
        attachment_input = tracker.get_slot("attachmentKeys")
        
        # Logic: If it's skipped or empty, make it an empty list. Otherwise, wrap it in a list.
        final_attachments = []
        if attachment_input:
            # Check if user typed a skip word
            if isinstance(attachment_input, str) and attachment_input.lower() in ["skip", "no", "ለማለፍ", "የለም", "none"]:
                final_attachments = []
            else:
                final_attachments = [attachment_input]
        
        # 3. Construct the JSON object
        incident_data = {
            "reference_number": reference_number,
            "title": tracker.get_slot("title"),
            "description": tracker.get_slot("description"),
            "source": "chatbot", # hardcoded or extracted
            "severity": tracker.get_slot("severity"),
            "region": tracker.get_slot("region"),
            "zone": tracker.get_slot("zone"),
            "woreda": tracker.get_slot("woreda"),
            "kebele": tracker.get_slot("kebele"),
            "specificArea": tracker.get_slot("specificArea"),
            "contactPhone": tracker.get_slot("contactPhone"),
            "occurredAt": tracker.get_slot("occurredAt"),
            "anonymity": tracker.get_slot("anonymity"),
            "latitude": "string", # Form doesn't ask this, left as string per requirement
            "longitude": "string",
            "attachmentKeys": final_attachments
        }

        # Print to console (This is where you would send data to your API)
        print(f"------------ NEW INCIDENT REPORT ------------")
        print(f"Ref: {reference_number}")
        print(f"Data: {incident_data}")
        print(f"---------------------------------------------")

        # 4. Send the confirmation message

        dispatcher.utter_message(text=f"ሪፖርትዎ በስኬት ተመዝግቧል። ለሚመለከተው ክፍል እናደርሳለን። የሪፖርት ሁኔታዎን በዚህ ቁጥር መከታተል ይችላሉ።\n\n {reference_number}")
        return [AllSlotsReset()]

    
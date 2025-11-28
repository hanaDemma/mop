# actions/actions.py
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted, Form
from rasa_sdk.forms import FormValidationAction
from typing import Any, Text, Dict, List   # ← This line was missing!


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

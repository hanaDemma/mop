from typing import Any, Text, Dict, List
import re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted

class ValidateFormGetLanguage(Action):
    def name(self) -> Text:
        return "validate_form_get_language"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Grab the latest text
        language = tracker.latest_message.get("text")

        supported = {"English", "አማርኛ", "Afaan Oromoo", "ትግርኛ"}

        if language in supported:
            return [SlotSet("selected_language", language)]
        else:
            dispatcher.utter_message(
                text="Sorry, I didn't recognize that language. Please choose from the options below."
            )
            dispatcher.utter_message(response="utter_ask_selected_language")
            return [SlotSet("selected_language", None)]


class ActionSubmitLanguageForm(Action):
    def name(self) -> Text:
        return "action_submit_language_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        lang = tracker.get_slot("selected_language")
        if not lang:
            dispatcher.utter_message(text="Language selection failed.")
            return []

        if lang == "English":
            dispatcher.utter_message(response="utter_greet_am")  # Replace with English utterances if needed
        elif lang == "አማርኛ":
            dispatcher.utter_message(response="utter_greet_am")
        elif lang == "Afaan Oromoo":
            dispatcher.utter_message(text="Afaan Oromoo greeting here")
        elif lang == "ትግርኛ":
            dispatcher.utter_message(text="Tigrinya greeting here")

        return [AllSlotsReset(), Restarted()]

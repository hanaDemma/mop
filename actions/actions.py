# actions/actions.py

import base64
import os
from xml.sax import make_parser
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, Restarted, Form
from rasa_sdk.forms import FormValidationAction
from typing import Any, Text, Dict, List   # ← This line was missing!
from datetime import datetime
import uuid  # <--- Add this at the top
from rasa_sdk.events import AllSlotsReset
import json
import requests
from PIL import Image
import io
from rasa_sdk.types import DomainDict




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
        valid = { "Amharic", "Afaan Oromoo", "Tigrinya", "Qafaraf","Somali"}
        return {"selected_language": slot_value if slot_value in valid else None}

class ActionSubmitLanguageForm(Action):
    def name(self) -> Text:
        return "action_submit_language_form"

    async def run(self, dispatcher, tracker, domain):
        lang = tracker.get_slot("selected_language")

        # Map the selected_language slot to the correct response suffixes
        # Ensure these match the language names in your buttons exactly!
        lang_mapping = {
            "Amharic": "am",
            "Afaan Oromoo": "oro",
            "Tigrinya": "tgr",
            "Qafaraf":"qrf",
            "Somali": "som",
            
        }

        suffix = lang_mapping.get(lang, "am") # Default to am if not found

        # 1. Greet the user
        dispatcher.utter_message(response=f"utter_greet_{suffix}")
        
        # 2. Show welcome message
        dispatcher.utter_message(response=f"utter_welcome_{suffix}")
        
        # 3. Show main menu
        dispatcher.utter_message(response=f"utter_main_menu_{suffix}")

        # IMPORTANT: Do NOT use AllSlotsReset() here yet, 
        # or the bot will forget the language it just set!
        return [AllSlotsReset()]

# # --- GLOBAL SETTINGS ---
# TELEGRAM_BOT_TOKEN = "8117533584:AAHWfcaqs7vFbE5rSpyGXWZU6b8LR-pjzYY"
# CEWRS_API_URL = "https://cewrs-api.aii.et/reports/public"

# class ActionSubmitIncidentForm(Action):
#     def name(self) -> Text:
#         return "action_submit_incident_form"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # 1. HANDLE ATTACHMENT (TELEGRAM IMAGE TO BASE64)
#         # We assume the slot 'attachmentKeys' contains the telegram 'file_id'
#         image_id = tracker.get_slot("attachmentKeys")
#         final_attachments = ["string"] # Default if no image
        
#         if image_id and isinstance(image_id, str):
#             # Check if user typed 'skip' words
#             skip_words = ["skip", "no", "none", "ለማለፍ", "የለም"]
#             if not any(word in image_id.lower() for word in skip_words):
#                 try:
#                     # A. Get File Path from Telegram
#                     file_info_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={image_id}"
#                     file_info = requests.get(file_info_url).json()
                    
#                     if file_info.get("ok"):
#                         file_path = file_info["result"]["file_path"]
                        
#                         # B. Download File
#                         download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
#                         image_raw = requests.get(download_url).content
                        
#                         # C. Encode to Base64 (Because Rasa/JSON needs text)
#                         encoded_img = base64.b64encode(image_raw).decode('utf-8')
#                         final_attachments = [encoded_img]
#                         print(f"DEBUG: Image successfully converted. Path: {file_path}")
#                 except Exception as e:
#                     print(f"DEBUG: Error processing image: {e}")

#         # 2. DATE FORMATTING (ISO 8601)
#         user_date = tracker.get_slot("occurredAt")
#         try:
#             # Fallback to current UTC if parsing fails
#             formatted_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
#         except:
#             formatted_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

#         # 3. CONSTRUCT PAYLOAD
#         incident_data = {
#             "title": tracker.get_slot("title"),
#             "description": tracker.get_slot("description"),
#             "severity": tracker.get_slot("severity"),
#             "source": "Chatbot",
#             "region": tracker.get_slot("region"),
#             "zone": tracker.get_slot("zone"),
#             "woreda": tracker.get_slot("woreda"),
#             "kebele": tracker.get_slot("kebele"),
#             "latitude": "string",
#             "longitude": "string",
#             "specificArea": tracker.get_slot("specificArea"),
#             "contactPhone": tracker.get_slot("contactPhone"),
#             "occurredAt": formatted_date,
#             "anonymity": bool(tracker.get_slot("anonymity")),
#             "attachmentKeys": final_attachments
#         }

#         # 4. POST TO CEWRS API
#         system_ref = "N/A"
#         try:
#             print("DEBUG: Sending data to CEWRS...")
#             response = requests.post(CEWRS_API_URL, json=incident_data, timeout=20)
            
#             if response.status_code in [200, 201]:
#                 res_json = response.json()
#                 # Accessing nested code from sourceData as per your previous debug output
#                 source_data = res_json.get("sourceData", {})
#                 system_ref = source_data.get("code", "SUCCESS")
#                 print(f"DEBUG: API Success! Ref: {system_ref}")
#             else:
#                 print(f"DEBUG: API Error {response.status_code}: {response.text}")
#                 system_ref = "Submission Error"

#         except Exception as e:
#             print(f"DEBUG: Connection failed: {e}")
#             system_ref = "Connection Failed"

#         # 5. FINAL CONFIRMATION (English/Amharic fallback)
#         lang = tracker.get_slot("selected_language")
#         if lang == "Amharic":
#             msg = f"ሪፖርትዎ በስኬት ተመዝግቧል። መለያ ቁጥርዎ፦ **{system_ref}** ነው።"
#         else:
#             msg = f"Your report has been submitted successfully. Reference Number: **{system_ref}**."

#         dispatcher.utter_message(text=msg)

#         return [AllSlotsReset()]


class ValidateIncidentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_incident_form"

    def validate_has_attachment(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value is False:
            # User said NO: Fill attachmentKeys with a dummy value to skip the ask
            return {"has_attachment": False, "attachmentKeys": "No Attachment"}
        
        # User said YES: Just set the bool and the bot will naturally ask for the file next
        return {"has_attachment": True}


class ActionSubmitIncidentForm(Action):
    def name(self) -> Text:
        return "action_submit_incident_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. DOWNLOAD, COMPRESS & ENCODE IMAGE
        image_id = tracker.get_slot("attachmentKeys")
        bot_token = "8117533584:AAHWfcaqs7vFbE5rSpyGXWZU6b8LR-pjzYY"
        
        # We start with the default "string" as per your sample
        final_attachments = ["string"] 

        if image_id and len(image_id) > 10:
            try:
                # Get path
                file_info = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile?file_id={image_id}").json()
                if file_info.get("ok"):
                    file_path = file_info["result"]["file_path"]
                    
                    # Download raw bytes
                    image_raw = requests.get(f"https://api.telegram.org/file/bot{bot_token}/{file_path}").content
                    
                    # --- COMPRESSION LOGIC ---
                    # Open image from bytes
                    img = Image.open(io.BytesIO(image_raw))
                    
                    # Convert to RGB (prevents errors if image has transparency)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # Resize if the image is too large (max 1024x1024)
                    img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    
                    # Save to memory buffer with compressed JPEG quality
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=75, optimize=True)
                    compressed_bytes = buffer.getvalue()
                    # -------------------------

                    # Encode the compressed bytes to Base64
                    encoded_string = base64.b64encode(compressed_bytes).decode('utf-8')
                    
                    # API expects a list of strings
                    final_attachments = [encoded_string]
                    print(f"DEBUG: Image compressed and base64 encoded successfully.")
            except Exception as e:
                print(f"DEBUG: Image processing/encoding failed: {e}")

        # 2. CONSTRUCT PURE JSON PAYLOAD
        desc = str(tracker.get_slot("description") or "No description provided")
        
        incident_data = {
            "title": str(tracker.get_slot("title") or "Untitled Report"),
            "description": desc,
            "severity": tracker.get_slot("severity") or "Medium",
            "source": "Chatbot",
            "region": tracker.get_slot("region"),
            "zone": tracker.get_slot("zone"),
            "woreda": tracker.get_slot("woreda"),
            "kebele": tracker.get_slot("kebele"),
            "latitude": "string",
            "longitude": "string",
            "specificArea": tracker.get_slot("specificArea"),
            "contactPhone": tracker.get_slot("contactPhone"),
            "occurredAt": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "anonymity": bool(tracker.get_slot("anonymity")),
            "attachmentKeys": final_attachments  # Now contains compressed base64
        }
        print("data is" , incident_data )
        # 3. POST AS JSON
        api_url = "https://cewrs-api.aii.et/reports/public"
        system_ref = "N/A"
        print("DEBUG: Sending payload to API...")

        try:
            response = requests.post(api_url, json=incident_data, timeout=30)
            
            if response.status_code in [200, 201]:
                res_json = response.json()
                source_data = res_json.get("sourceData", {})
                system_ref = source_data.get("code", "SUCCESS")
                print(f"DEBUG: API Success! Ref: {system_ref}")
            else:
                print(f"DEBUG: API Error {response.status_code}: {response.text}")
                system_ref = "Submission Error"

        except Exception as e:
            print(f"DEBUG: Connection failed: {e}")
            system_ref = "Connection Failed"

        # 4. RESPONSE
        dispatcher.utter_message(text=f"ሪፖርትዎ በስኬት ተመዝግቧል። መለያ ቁጥርዎ፦ {system_ref} ነው።")

        return [AllSlotsReset()]
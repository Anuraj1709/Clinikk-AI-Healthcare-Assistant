import json
import uuid
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

LEADS_FILE = DATA_DIR / "leads.json"

if not LEADS_FILE.exists():
    with open(LEADS_FILE, "w") as f:
        json.dump([], f, indent=4)


class SalesforceManager:

    def __init__(self):
        pass


    def load_leads(self):

        with open(LEADS_FILE, "r") as f:

            return json.load(f)


    def save_leads(self, data):

        with open(LEADS_FILE, "w") as f:

            json.dump(data, f, indent=4)

    def save_patient(self, state, lead_result):

        leads = self.load_leads()

        lead_id = str(uuid.uuid4())

        lead_score = lead_result["score"]

        temperature = lead_result["temperature"]

        record = {

            "lead": {

                "lead_id": lead_id,

                "created_at": datetime.now().isoformat(),

                "lead_score": lead_score,

                "temperature": temperature,

                "patient_type": state["patient_type"],

                "status": "Open",

                "lead_source": "AI Chatbot",

                "name": state["lead"].get("name"),

                "phone": state["lead"].get("phone"),

                "email": state["lead"].get("email"),

                "preferred_clinic": state["lead"].get("clinic"),

                "preferred_date": state["lead"].get("date"),

                "reason": state["lead"].get("reason")

            },

            "task": {

                "subject": "Healthcare AI Conversation",

                "status": "Completed",

                "priority": "High" if temperature == "Hot" else "Normal",

                "conversation": state["messages"]

            }

        }

        leads.append(record)

        self.save_leads(leads)

        print("Lead stored locally")

        return True
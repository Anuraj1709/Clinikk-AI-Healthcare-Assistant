from typing import Dict

conversation_store: Dict = {}


def get_state(session_id: str):

    if session_id not in conversation_store:

        conversation_store[session_id] = {

            "intent": None,

            "stage": None,

            "patient_type": None,

            "lead": {

                "name": None,

                "phone": None,

                "email": None,

                "clinic": None,

                "doctor": None,

                "date": None,

                "reason": None

            },

            "messages": []

        }

    return conversation_store[session_id]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from salesforce import SalesforceManager

from models import ChatRequest
from chat_engine import generate_answer
from intent_classifier import classify_intent
from conversation_manager import get_state
from appointment import handle_appointment


app = FastAPI(
    title="Healthcare AI Agent",
    version="1.0"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


@app.get("/")
def home():

    return {

        "status": "running",

        "application": "Healthcare AI Agent"

    }


@app.post("/chat")
def chat(request: ChatRequest):


    state = get_state(request.session_id)


    state["messages"].append(

        {

            "role": "user",

            "content": request.message

        }

    )

    if (

        state["stage"] is not None

        and

        state["stage"] != "completed"

    ):

        response = handle_appointment(

            state,

            request.message

        )

    else:

        classification = classify_intent(
            request.message
        )

        intent = classification["intent"]

        patient_type = classification["patient_type"]

        if (
            patient_type != "unknown"
            and state["patient_type"] is None
        ):

            state["patient_type"] = patient_type

        if intent == "appointment":

            response = handle_appointment(
                state,
                request.message
            )

        else:

            response = generate_answer(
                request.message
            )


    state["messages"].append(

        {

            "role": "assistant",

            "content": response

        }

    )


    return {

        "response": response,

        "patient_type": state["patient_type"],

        "stage": state["stage"]

    }

@app.get("/leads")
def get_all_leads():

    sf = SalesforceManager()

    return sf.load_leads()


@app.get("/analytics")
def analytics():

    sf = SalesforceManager()

    leads = sf.load_leads()

    total = len(leads)

    hot = sum(
        1 for x in leads
        if x["lead"]["temperature"] == "Hot"
    )

    warm = sum(
        1 for x in leads
        if x["lead"]["temperature"] == "Warm"
    )

    cold = sum(
        1 for x in leads
        if x["lead"]["temperature"] == "Cold"
    )

    return {

        "total_leads": total,

        "hot": hot,

        "warm": warm,

        "cold": cold

    }
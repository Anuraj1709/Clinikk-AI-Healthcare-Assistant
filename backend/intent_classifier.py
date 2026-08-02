import json
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


def classify_intent(message: str):
    """
    Classify the user's intent and patient type.

    Returns:
    {
        "intent": "...",
        "patient_type": "..."
    }
    """

    prompt = f"""
You are an AI assistant for a healthcare clinic.

Analyze the user's message and determine:

1. Intent
2. Patient Type

Possible intents:
- faq
- appointment
- general

Patient Type:
- new
- existing
- unknown

Rules:

- If the user mentions they have visited before,
  had a previous consultation,
  follow-up,
  returning patient,
  existing member,
  previous appointment,
  return "existing".

- If the user clearly says this is their first visit,
  first consultation,
  never visited,
  return "new".

- If there isn't enough information,
  return "unknown".

Examples:

User:
I want to know your membership plans.

Output:
{{
"intent":"faq",
"patient_type":"unknown"
}}

----------------------------

User:
I visited your clinic last month.

Output:
{{
"intent":"general",
"patient_type":"existing"
}}

----------------------------

User:
I need a follow-up consultation.

Output:
{{
"intent":"appointment",
"patient_type":"existing"
}}

----------------------------

User:
This will be my first consultation.

Output:
{{
"intent":"appointment",
"patient_type":"new"
}}

----------------------------

User:
I want to book an appointment.

Output:
{{
"intent":"appointment",
"patient_type":"unknown"
}}

Now analyze this message:

{message}

Return ONLY valid JSON.

"""

    try:

        response = llm.invoke(prompt)

        result = json.loads(response.content)

        return result

    except Exception as e:

        print("Intent Classification Error:", e)

        return {
            "intent": "general",
            "patient_type": "unknown"
        }
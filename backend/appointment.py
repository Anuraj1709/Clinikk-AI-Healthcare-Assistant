import re

from lead_scoring import calculate_lead_temperature
from salesforce import SalesforceManager


sf = SalesforceManager()

def validate_phone(phone: str):

    phone = phone.strip()

    if re.fullmatch(r"[6-9]\d{9}", phone):
        return True

    return False


def validate_email(email: str):

    email = email.strip()

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if re.fullmatch(pattern, email):
        return True

    return False


def format_success():

    return (
        "Thank you! Your appointment request has been submitted successfully.\n\n"
        "Our care team will contact you shortly to confirm your appointment."
    )

def handle_appointment(state, message):

    lead = state["lead"]

    stage = state["stage"]

    patient_type = state["patient_type"]

    message = message.strip()


    if stage is None:

        if patient_type == "new":

            state["stage"] = "name"

            return (
                "Welcome to Clinikk! 😊\n\n"
                "Let's schedule your appointment.\n\n"
                "May I know your full name?"
            )

        elif patient_type == "existing":

            state["stage"] = "phone"

            return (
                "Welcome back! 😊\n\n"
                "Please enter your registered mobile number."
            )

        else:

            state["stage"] = "patient_type"

            return (
                "Sure! I'd be happy to help you schedule an appointment.\n\n"
                "Have you visited Clinikk before?\n\n"
                "Please reply with:\n"
                "Yes\n"
                "or\n"
                "No"
            )

    if stage == "patient_type":

        answer = message.lower()

        if answer == "yes":

            state["patient_type"] = "existing"

            state["stage"] = "phone"

            return (
                "Great!\n\n"
                "Please enter your registered mobile number."
            )

        elif answer == "no":

            state["patient_type"] = "new"

            state["stage"] = "name"

            return (
                "Wonderful!\n\n"
                "Please tell me your full name."
            )

        else:

            return "Please reply only with Yes or No."

    if stage == "name":

        lead["name"] = message

        state["stage"] = "phone"

        return (
            f"Nice to meet you, {message}! 😊\n\n"
            "Please enter your 10-digit mobile number."
        )


    if stage == "phone":

        if not validate_phone(message):

            return (
                "Please enter a valid 10-digit Indian mobile number."
            )

        lead["phone"] = message

        if state["patient_type"] == "new":

            state["stage"] = "email"

            return "Please enter your email address."

        state["stage"] = "clinic"

        return (
            "Which Clinikk location would you prefer?\n\n"
            "Example:\n"
            "Koramangala\n"
            "HSR Layout\n"
            "Indiranagar"
        )


    if stage == "email":

        if not validate_email(message):

            return "Please enter a valid email address."

        lead["email"] = message

        state["stage"] = "clinic"

        return (
            "Which Clinikk location would you prefer?\n\n"
            "Example:\n"
            "Koramangala\n"
            "HSR Layout\n"
            "Indiranagar"
        )


    if stage == "clinic":

        lead["clinic"] = message

        state["stage"] = "date"

        return (
            "Great!\n\n"
            "What is your preferred appointment date?\n\n"
            "Example:\n"
            "2026-08-10\n"
            "or\n"
            "Tomorrow Morning"
        )

    if stage == "date":

        lead["date"] = message

        state["stage"] = "reason"

        return (
            "Could you briefly describe the reason for your visit?\n\n"
            "Examples:\n"
            "- Fever\n"
            "- Diabetes Consultation\n"
            "- General Checkup\n"
            "- Follow-up Consultation"
        )

    if stage == "reason":

        lead["reason"] = message

    
        lead_result = calculate_lead_temperature(state)

        print(f"Lead Score: {lead_result['score']}")
        print(f"Lead Temperature: {lead_result['temperature']}")

        # Save to local CRM (leads.json)
        saved = sf.save_patient(
            state,
            lead_result
        )

        state["stage"] = "completed"

        if saved:

            return (
                "Thank you! Your appointment request has been submitted successfully.\n\n"
                "Our care team will contact you shortly to confirm your appointment."
            )

        return (
            "We couldn't save your appointment request. Please try again later."
        )

    if stage == "completed":

        return (
            "Your appointment request has already been submitted.\n\n"
            "If you'd like to book another appointment, please start a new conversation."
        )

    return (
        "Sorry, something went wrong while processing your appointment."
    )
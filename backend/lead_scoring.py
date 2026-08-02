def calculate_lead_temperature(state):
    """
    Calculate lead quality based on how much information
    the user has shared.
    """

    lead = state["lead"]

    score = 0

    if lead["name"]:
        score += 15

    if lead["phone"]:
        score += 20

    if lead["email"]:
        score += 15

    if lead["clinic"]:
        score += 15

    if lead["date"]:
        score += 15

    if lead["reason"]:
        score += 20

    # Existing patients are generally more likely to convert
    if state["patient_type"] == "existing":
        score += 10

    if score >= 80:
        return {
                "score": score,
                "temperature": "Hot"
            }

    elif score >= 45:
        return {
                "score": score,
                "temperature": "Warm"
            }

    return {
        "score": score,
        "temperature": "Cold"
    }
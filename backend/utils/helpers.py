def validate_request(data):
    required_fields = ['preferences', 'days', 'budget']
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    if len(data['preferences']) != 5:
        return False, "Preferences must have 5 values"
    return True, ""

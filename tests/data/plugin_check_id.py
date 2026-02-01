from typing import Any, Dict, List

def validate(data: Dict[str, Any]) -> List[str]:
    """
    Example plugin: Checks if ID starts with 'PROBAND'.
    """
    errors = []
    pid = data.get("id")
    if pid and not pid.startswith("PROBAND"):
        errors.append(f"Custom Rule: ID '{pid}' does not start with 'PROBAND'")
    
    # Check age consistency if present
    # (Just a dummy rule for testing)
    subject = data.get("subject", {})
    age = subject.get("timeAtLastEncounter", {}).get("age", {}).get("iso8601duration")
    if age and "Y" not in age:
        errors.append("Custom Rule: Age must be in years (e.g., P25Y)")
        
    return errors

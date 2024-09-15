import json

# Function to load user preferences from a file
def load_preferences(file_path="preferences.json"):
    try:
        with open(file_path, "r") as f:
            preferences = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default preferences if the file doesn't exist or is invalid
        preferences = {"cams": [
                            {"url": None, "id": 0, "size": None, "fps": None},
                            {"url": None, "id": 1, "size": None, "fps": None},
                            {"url": None, "id": 2, "size": None, "fps": None},
                            {"url": None, "id": 3, "size": None, "fps": None},
                       ]}
    return preferences

# Function to save user preferences to a file
def save_preferences(preferences, file_path="preferences.json"):
    with open(file_path, "w") as f:
        json.dump(preferences, f, indent=4)

    # Notebook Camera Setup
    #
    # Cam(
    #     0,
    #     #ID,
    #     (800, 600),
    #     11
    # )

    # IP Camera Setup
    #
    # Cam(
    #     "rtsp://admin:TaekwondoVAR@169.254.1.1:554",
    #     #ID,
    #     (1200, 800),
    #     30
    # )
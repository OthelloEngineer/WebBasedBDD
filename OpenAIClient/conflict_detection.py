# conflict_detection.py

import os
import openai
from data import Context, NewResponse
from dotenv import load_dotenv

load_dotenv()

def detect_conflicts(bdd_text, model_version="gpt-3.5-turbo"):
    """
    Uses the OpenAI API to detect conflicts in the given BDD text.

    Parameters:
        bdd_text (str): The BDD scenarios as a string.
        model_version (str): The OpenAI model version to use.

    Returns:
        str: The conflicts identified in the BDD scenarios.
    """
    openai_api_key = os.environ.get("OPEN_AI_TOKEN")
    if not openai_api_key:
        raise ValueError("OPEN_AI_TOKEN environment variable not found.")
    openai.api_key = openai_api_key

    # Prepare the conversation context
    context = [
        Context(
            role="system",
            content="You are an assistant that identifies conflicts in BDD scenarios."
        ),
        Context(
            role="user",
            content=(
                "Please analyze the following BDD scenarios and identify any potential conflicts, "
                "such as two tasks involving the same object:\n\n" + bdd_text
            )
        )
    ]

    # Convert Context objects to dictionaries.
    messages = [{"role": c.role, "content": c.content} for c in context]

    # Call the OpenAI API
    response = openai.chat.completions.create(
        model=model_version,
        messages=messages
    )      

    # Extract the assistant's reply
    conflicts = response.choices[0].message.content.strip()
    return conflicts

if __name__ == "__main__":
    # BDD examples as a multi-line string
    bdd_text = """
EXAMPLE 1:
declarative entity robot {
actions: moves, grabs, releases
properties: position
}
declarative entity object {
states: grabbed, released
}
Scenario: "grabbing object"
Given the position of the robot "Sun" is "START"
When the robot "Sun" moves to position "aboveObject"
And the robot "Sun" grabs the object "Bottle"
Then the object "Bottle" is grabbed
Scenario: "moving object"
Given the object "Bottle" is grabbed
When the robot "Sun" moves to position "above bucket"
And the robot "Sun" releases the object "Bottle"
Then the object "Bottle" is released

EXAMPLE 2:
declarative entity robot {
actions: moves, picks, releases
properties: position
}
declarative entity object {
states: sensed, sorted
}
declarative entity sensor {
states: active, inactive
}
Scenario: "Sensing object"
Given the sensor "Sensor" is active
When the robot "Bob" picks the object "Ball"
And the robot "Bob" moves to position "SENSOR_AREA"
Then the object "Ball” is sensed
Scenario: "Sorting object"
Given the color of the object "Ball" is "green"
And the sensor "Sensor" is active
When the robot "Bob" moves to position "GREEN_BUCKET"
And the robot "Bob" releases the object "Ball"
Then the object "Ball" is sorted

EXAMPLE 3:
declarative entity robot {
actions: moves, picks, releases
properties: position, speed
}
declarative entity output {
states: ON, OFF
actions: activates, deactivates
properties: position
}
declarative entity button {
states: ON, OFF
properties: signal
}
declarative entity gripper {
states: open, closed
actions: opens, closes
}
Scenario: "PickAndPlace1"
Given the output "light" is OFF
And the gripper "gripper" is closed
And the signal of the button "greenButton" is ON
When the output "light" activates
And the robot "Rob" linearly moves to position "aboveObject"
And the gripper "gripper" opens
Then the position of the robot "Rob" is "aboveObject"
And the gripper "gripper" is open
Scenario: "PickAndPlace2"
Given the position of the robot "Rob" is "aboveObject"
And the gripper "gripper" is open
When the gripper "gripper" closes
And the robot "Rob" moves to position "placementLocation" with "fast” speed
And the gripper "gripper" opens
And the output "light" deactivates
Then the output "light" is OFF
And the position of the robot "Rob" is "placementLocation"
And the gripper "gripper" is open
"""

# Detect conflicts in the BDD text
conflicts = detect_conflicts(bdd_text)
print("Potential Conflicts Found:")
print(conflicts)

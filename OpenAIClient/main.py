import os
import openai
import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, HTTPException
from starlette.middleware.cors import CORSMiddleware

from change_tracker import tracker
from data import NewResponse, Context
from dependency_manager import Scenario, ScenarioDependencyResponse, AllDependenciesResponse, DependencyManager

load_dotenv()

app = FastAPI(debug=True)
router = APIRouter()


def get_new_message(context: list[Context], model_version, new_message, user):
    """
    Generates a response from the OpenAI API based on the provided context and new message.

    Parameters:
        context (list): A list of Context objects representing the conversation history.
        model_version (str): The model version to use (e.g., 'gpt-3.5-turbo', 'gpt-4').
        new_message (str): The latest message input from the user.
        user (str): The role of the user, typically "user".

    Returns:
        str: The generated response from the OpenAI API.
    """

    openai_api_key = os.environ.get("OPEN_AI_TOKEN")
    if not openai_api_key:
        raise ValueError("OPEN_AI_TOKEN environment variable not found.")
    openai.api_key = openai_api_key

    new_message_context = Context(role=user, content=new_message)
    context.append(new_message_context)

    messages = [{"role": c.role, "content": c.content} for c in context]

    print(messages)
    response = openai.chat.completions.create(
        model=model_version,
        messages=messages
    )
    print(response)
    choice = response.choices[0].message.content
    print(choice)
    return choice

    # Extract the assistant's reply
    # assistant_reply = response['choices'][0]['message']['content'].strip()

    # Append the assistant's reply to the context
    # context.append({"role": "assistant", "content": assistant_reply})


#
# return assistant_reply


@router.post("/get_response")
async def get_response(new_response: NewResponse):
    """
    example request:
    {
		"message": "Who was the MVP of that series?",
		"context": [
				{"role": "user", "content": "You are a helpful assistant."},
				{"role": "user", "content": "Hello, who won the World Series in 2020?"},
				{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}
		],
		"user": "user",
		"model": "o1-preview-2024-09-12"
}
    """
    print(new_response)
    new_gippity = get_new_message(
        new_response.context,
        new_response.model,
        new_response.message,
        new_response.user
    )
    print(new_gippity)
    return {"response": new_gippity}


if __name__ == "1__main__":
    context = [
        {"role": "user", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, who won the World Series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    ]
    model_version = "gpt-3.5-turbo"
    new_message = "Who was the MVP of that series?"
    # response = get_new_message(context, model_version, new_message)
    # print(response)


@router.get("/get_changes/{file_name}")
async def get_changes(file_name: str):
    """
    example request:
    {
        "file_name": "sample.bdd"
    }
    """
    print(f"File name: {file_name}")
    if file_name is None or file_name == "":
        return {"message": "Please provide a file name."}

    changes = tracker.get_file_changes(file_name)
    print(f"Changes: {changes}")
    return changes


@router.post("/track_changes")
async def track_changes():
    tracker.track_changes()
    return {"message": "Changes have been tracked."}


@router.post("/set_actor")
async def set_actor(actor_name: str, actor_email: str):
    tracker.set_actor(actor_name, actor_email)
    return {"message": f"Actor has been set to {actor_name}."}


@router.get("/get_actor")
async def get_actor():
    return {"actor_name": tracker.actor_name, "actor_email": tracker.actor_email}


@router.get("/get_changes")
async def get_all_changes():
    commits = tracker.get_changes()
    return commits


# DependencyManager endpoints
@router.post("/add_scenario", response_model=Scenario)
async def add_scenario(scenario: Scenario):
    """
    Adds a new scenario to the DependencyManager.
    """
    new_scenario = Scenario(
        id=DependencyManager.next_id,
        title=Scenario.title,
        content=Scenario.content,
        dependencies=Scenario.dependencies
    )
    DependencyManager.scenarios[new_scenario.id] = new_scenario
    DependencyManager.next_id += 1
    return new_scenario


@router.post("/add_dependency")
async def add_dependency(scenario_id: int, depends_on_id: int):
    """
    Adds a dependency between two scenarios.
    """
    try:
        DependencyManager.set_dependency(scenario_id, depends_on_id)
        return {"message": f"Scenario {scenario_id} now depends on Scenario {depends_on_id}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_dependencies/{scenario_id}", response_model=ScenarioDependencyResponse)
async def get_dependencies(scenario_id: int):
    """
    Retrieves dependencies for a specific scenario.
    """
    scenario = DependencyManager.get_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return ScenarioDependencyResponse(
        scenario_id=scenario_id,
        dependencies=scenario.dependencies
    )


@router.get("/get_all_dependencies", response_model=AllDependenciesResponse)
async def get_all_dependencies():
    """
    Retrieves all scenarios and their dependencies.
    """
    all_dependencies = {
        scenario.id: scenario.dependencies for scenario in DependencyManager.scenarios.values()
    }
    return AllDependenciesResponse(dependencies=all_dependencies)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

if __name__ == "__main__":
    app.include_router(router)
    uvicorn.run(app, host="localhost", port=8000)

import json
from google import genai
from pydantic import BaseModel
from typing import List
from prompts import SCENE_EXTRACTION_PROMPT

# The client uses the GOOGLE_API_KEY environment variable automatically
client = genai.Client()


# Define the Pydantic model for a scene
class Scene(BaseModel):
    scene_number: int
    description: str
    characters: List[str]


# Define the Pydantic model for a list of scenes
class SceneList(BaseModel):
    scenes: List[Scene]


def generate_scenes():
    """Extracts scenes from the story."""
    # Read the story from the documents directory
    with open("md_files/story.md", "r") as f:
        story_text = f.read()

    # Create a prompt to extract scenes from the story
    scene_extraction_prompt = SCENE_EXTRACTION_PROMPT.format(story_text=story_text)

    # Generate the structured scene data
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=scene_extraction_prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": SceneList,
        },
    )

    # Save the scene data to a JSON file
    with open("json_files/scenes.json", "w") as f:
        f.write(response.text)

    print("Scenes extracted and saved to json_files/scenes.json")


if __name__ == "__main__":
    generate_scenes()

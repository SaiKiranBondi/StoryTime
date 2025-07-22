from google import genai
import os
import json
from pydantic import BaseModel
from typing import List
from prompts import STORY_GENERATION_PROMPT, CHARACTER_EXTRACTION_PROMPT

# The client uses the GOOGLE_API_KEY environment variable automatically
client = genai.Client()


# Define the Pydantic model for a character
class Character(BaseModel):
    name: str
    description: str


# Define the Pydantic model for a list of characters
class CharacterList(BaseModel):
    characters: List[Character]


def generate_story():
    """Generates a story and extracts characters."""
    # Generate the content
    response = client.models.generate_content(
        model="gemini-2.5-pro", contents=STORY_GENERATION_PROMPT
    )

    if not os.path.exists("md_files"):
        os.makedirs("md_files")

    # Save the story to a file
    story_text = response.candidates[0].content.parts[0].text
    with open("md_files/story.md", "w") as f:
        f.write(story_text)

    print("Story generated and saved to story.md")

    # Create a prompt to extract characters from the story
    character_extraction_prompt = CHARACTER_EXTRACTION_PROMPT.format(
        story_text=story_text
    )

    # Generate the structured character data
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=character_extraction_prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CharacterList,
        },
    )

    if not os.path.exists("json_files"):
        os.makedirs("json_files")

    # Save the character data to a JSON file
    with open("json_files/characters.json", "w") as f:
        f.write(response.text)

    print("Characters extracted and saved to json_files/characters.json")


if __name__ == "__main__":
    generate_story()

import json
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from prompts import CHARACTER_IMAGE_PROMPT

# The client uses the GOOGLE_API_KEY environment variable automatically
client = genai.Client()


def generate_character_images():
    """Generates images for each character."""
    # Load the character data
    with open("json_files/characters.json", "r") as f:
        character_data = json.load(f)

    # Create the Image_generated directory if it doesn't exist in the parent folder
    image_dir = "Image_generated"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    character_image_mapping = {}

    # Generate an image for each character
    for character in character_data["characters"]:
        character_name = character["name"]
        character_description = character["description"]

        print(f"Generating image for {character_name}...")

        # Create a prompt for the image generation
        image_prompt = CHARACTER_IMAGE_PROMPT.format(
            character_name=character_name, character_description=character_description
        )

        # Generate the image
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=image_prompt,
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )

        # Sanitize the character name for the filename
        safe_character_name = character_name.replace(" ", "_")
        image_path = os.path.join(image_dir, f"{safe_character_name}.png")

        # Save the image
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                image.save(image_path)
                print(f"Image for {character_name} saved to {image_path}")
                # Store the mapping from original name to new filename
                character_image_mapping[character_name] = f"{safe_character_name}.png"

    # Save the mapping to a file in the json_files directory
    with open("json_files/character_image_mapping.json", "w") as f:
        json.dump(character_image_mapping, f, indent=4)

    print("Character image mapping saved to json_files/character_image_mapping.json")


if __name__ == "__main__":
    generate_character_images()

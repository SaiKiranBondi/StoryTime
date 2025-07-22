import json
import os
import io
from PIL import Image
from google import genai
from google.genai import types
from prompts import SCENE_IMAGE_PROMPT

# The client uses the GOOGLE_API_KEY environment variable automatically
client = genai.Client()


def generate_scene_images():
    """Generates images for each scene."""
    # --- 1. Setup: Load data and create directories ---

    # Create Scene_Images directory if it doesn't exist
    if not os.path.exists("Scene_Images"):
        os.makedirs("Scene_Images")

    # Define the path to the Image_generated directory
    image_dir = "Image_generated"

    # Check if the Image_generated directory exists
    if not os.path.exists(image_dir):
        print(
            f"Error: The '{image_dir}' directory does not exist. Please run the character generation script first."
        )
        exit()

    # Load scenes, characters, and the image mapping
    try:
        with open("json_files/scenes.json", "r") as f:
            scenes_data = json.load(f)
        with open("json_files/character_image_mapping.json", "r") as f:
            character_image_mapping = json.load(f)
    except FileNotFoundError as e:
        print(
            f"Error: {e.filename} not found. Please ensure that scenes.json and character_image_mapping.json exist in the json_files directory."
        )
        exit()

    # --- 2. Scene Image Generation ---

    # Process each scene
    for scene in scenes_data.get("scenes", []):
        scene_number = scene.get("scene_number")
        scene_description = scene.get("description")
        scene_characters = scene.get("characters", [])

        if not all([scene_number, scene_description]):
            print("Skipping a scene due to missing number or description.")
            continue

        print(f"--- Processing Scene {scene_number} ---")

        # --- 2a. Create Character Reference Sheet ---
        character_images = []
        for character_name in scene_characters:
            # Get the sanitized filename from the mapping
            image_filename = character_image_mapping.get(character_name)
            if not image_filename:
                print(
                    f"Warning: Mapping for character '{character_name}' not found in character_image_mapping.json. Skipping this character."
                )
                continue

            image_path = os.path.join(image_dir, image_filename)
            if os.path.exists(image_path):
                character_images.append(Image.open(image_path))
            else:
                print(
                    f"Warning: Image for character '{character_name}' not found at {image_path}. Skipping this character."
                )

        if not character_images:
            print(
                f"Skipping scene {scene_number}: No character images found for the characters in this scene."
            )
            continue

        # Create a composite image (reference sheet)
        widths, heights = zip(*(i.size for i in character_images))
        total_width = sum(widths)
        max_height = max(heights)
        composite_image = Image.new("RGB", (total_width, max_height))

        x_offset = 0
        for img in character_images:
            composite_image.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        print(f"Generated character reference sheet for Scene {scene_number}.")

        # --- 2b. Generate Final Scene Image ---
        scene_prompt = SCENE_IMAGE_PROMPT.format(scene_description=scene_description)

        print(f"Generating final image for Scene {scene_number}...")

        # Generate the image using the multi-modal model
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[scene_prompt, composite_image],
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )

        # Save the generated scene image
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    scene_image = Image.open(io.BytesIO(image_data))
                    scene_image.save(f"Scene_Images/scene_{scene_number}.png")
                    print(
                        f"Successfully saved image for Scene {scene_number} to Scene_Images/scene_{scene_number}.png"
                    )
                    break

    print("--- All scenes processed. ---")


if __name__ == "__main__":
    generate_scene_images()

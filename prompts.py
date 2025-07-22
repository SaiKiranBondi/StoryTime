STORY_GENERATION_PROMPT = (
    "Write a short story about a puppy who rescues a kitten from strom."
)

CHARACTER_EXTRACTION_PROMPT = """
Based on the following story, identify the main characters and provide a brief description of each.

Story:
{story_text}
"""

SCENE_EXTRACTION_PROMPT = """
Based on the following story, identify 3-5 key scenes that are suitable for illustration. For each scene, provide a brief description and a list of the characters present.

Story:
{story_text}
"""

CHARACTER_IMAGE_PROMPT = "A portrait of {character_name}, {character_description}. Consistent character design."

SCENE_IMAGE_PROMPT = """
Illustrate the following scene: {scene_description}. 
Ensure the characters in the scene are consistent with the provided character reference image.
"""

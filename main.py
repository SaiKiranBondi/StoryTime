from generate_story import generate_story
from generate_scenes import generate_scenes
from generate_character_images import generate_character_images
from generate_scene_images import generate_scene_images

def main():
    """Runs the full story generation and image creation pipeline."""
    print("--- Starting Story Generation ---")
    generate_story()
    print("--- Finished Story Generation ---\n")

    print("--- Starting Scene Extraction ---")
    generate_scenes()
    print("--- Finished Scene Extraction ---")

    print("--- Starting Character Image Generation ---")
    generate_character_images()
    print("--- Finished Character Image Generation ---")

    print("--- Starting Scene Image Generation ---")
    generate_scene_images()
    print("--- Finished Scene Image Generation ---")

if __name__ == '__main__':
    main()
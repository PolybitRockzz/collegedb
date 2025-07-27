import os
import subprocess


def run_image_parser(image_path: str, vision_model: str, prompt_file: str = 'parser.txt') -> str:
    """
    Run an Ollama vision model on the given image using a text prompt file and save the generated output as a markdown file.

    Args:
        image_path: Path to the input image file.
        vision_model: Ollama model name to use for vision parsing.
        prompt_file: Path to a text file containing the prompt (default: 'parser.txt').

    Returns:
        Path to the generated markdown file in the temp directory.
    """
    # Ensure temp directory exists
    base_dir = os.path.dirname(__file__)
    temp_dir = os.path.join(base_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    # Build and run the Ollama command by passing the prompt via stdin
    with open(prompt_file, 'r', encoding='utf-8') as pf:
        prompt_text = pf.read()
    cmd = [
        'ollama', 'run', vision_model
    ]
    result = subprocess.run(
        cmd,
        input=prompt_text.replace("<<IMAGEPATH>>", image_path),
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.returncode != 0:
        raise RuntimeError(f"Ollama run failed with error:\n{result.stderr}")

    output = result.stdout

    # Write output to markdown file
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    md_filename = f"{image_name}.md"
    md_path = os.path.join(temp_dir, md_filename)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(output)

    return md_path
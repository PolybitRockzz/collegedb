import os
import subprocess
from typing import Optional, List, Dict


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
    # Remove leading and trailing code fence markers ```
    lines = output.splitlines()
    if lines and lines[0].startswith("```markdown"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    output = "\n".join(lines)

    # Write or append output to a markdown file named after the PDF base name
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    # Derive PDF base name before page suffix (_pageN)
    pdf_base = image_name.split('_page')[0]
    md_filename = f"{pdf_base}.md"
    md_path = os.path.join(temp_dir, md_filename)
    # Append output to markdown file
    with open(md_path, 'a', encoding='utf-8') as f:
        f.write(output)
        f.write("\n\n")  # Separate pages with blank line
    return md_path

def run_markdown_linter(pdf_base: str, temp_dir: str, linter_model: str, linter_prompt_text: Optional[str] = None) -> List[str]:
    """
    Run an Ollama linter model on the combined markdown for a PDF and split into chapter files.
    Generates a JSON array with elements {"filename": ..., "content": ...}.
    Writes each element to a separate markdown file in temp_dir.
    Also saves the linter prompt to a .txt file.
    Returns a list of created markdown file paths.
    """
    import json
    # Read combined markdown
    md_file = os.path.join(temp_dir, f"{pdf_base}.md")
    if not os.path.exists(md_file):
        raise FileNotFoundError(f"Markdown file not found: {md_file}")
    with open(md_file, 'r', encoding='utf-8') as mf:
        markdown_content = mf.read()

    # Load linter prompt from linter.txt
    base_dir = os.path.dirname(__file__)
    linter_prompt_file = os.path.join(base_dir, 'linter.txt')
    if not os.path.exists(linter_prompt_file):
        raise FileNotFoundError(f"Linter prompt file not found: {linter_prompt_file}")
    with open(linter_prompt_file, 'r', encoding='utf-8') as pf:
        prompt_text = pf.read()

    # Save the prompt used for linting
    prompt_file_path = os.path.join(temp_dir, f"{pdf_base}_linter_prompt.txt")
    with open(prompt_file_path, 'w', encoding='utf-8') as pf:
        pf.write(prompt_text)

    # Prepare input by replacing placeholder
    input_text = prompt_text.replace("<<CONTENT>>", markdown_content)

    # Invoke Ollama linter model
    cmd = ['ollama', 'run', linter_model]
    result = subprocess.run(cmd, input=input_text, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Ollama linter failed: {result.stderr}")

    # Parse JSON output
    try:
        chapters = json.loads(result.stdout)
    except Exception as e:
        raise ValueError(f"Invalid JSON from linter: {e}\n{result.stdout}")

    created_files = []
    # Write each chapter to its own markdown file
    for chapter in chapters:
        fname = chapter.get('filename')
        content = chapter.get('content', '')
        if not fname:
            continue
        safe_name = f"{fname}.md"
        out_path = os.path.join(temp_dir, safe_name)
        with open(out_path, 'w', encoding='utf-8') as of:
            of.write(content)
        created_files.append(out_path)

    return created_files
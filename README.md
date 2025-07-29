<h1 align="center" style="text-align: center; font-size: 35px; font-weight: 700;">College DB + AI 🤖</h1>

<p align="center" style="text-align: center; font-size: 16px;">A python automation for college notes and PYQs.</p>

> [!IMPORTANT]
> This project is a work in progress.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/PolybitRockzz/collegedb.git
   cd collegedb
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv env  # Create virtual env
   # Windows PowerShell:
   env\Scripts\Activate.ps1
   # Unix/macOS:
   # source env/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies for PDF conversion (pdf2image):

   * Windows: download and install Poppler from https://blog.alivate.com.au/poppler-windows/
   * Linux/macOS: `sudo apt-get install poppler-utils` or `brew install poppler`

5. Install Ollama CLI and required models:

   ```bash
   # Follow instructions at https://ollama.com/
   ollama install llama3
   ollama install qwen2.5vl:7b
   ```

6. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

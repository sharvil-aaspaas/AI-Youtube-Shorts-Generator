
## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg
- OpenCV

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator.git
   cd AI-Youtube-Shorts-Generator
   ```

2. Create a virtual environment

```bash
python3.10 -m venv venv
```

3. Activate a virtual environment:

```bash
source venv/bin/activate # On Windows: venv\Scripts\activate
```

4. Install the python dependencies:

```bash
pip install -r requirements.txt
```

---

1. Set up the environment variables.

Create a `.env` file in the project root directory and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Usage

1. Ensure your `.env` file is correctly set up with your Anthropic API key.
2. Run the main script and enter the desired YouTube URL when prompted:
   ```bash
   python main.py
   ```

A Streamlit-based AI assistant powered by **Google Gemini 1.5 Flash**.
This tool helps manufacturing employees understand Standard Operating Procedures (SOPs) and safety rules (LOTO, PPE, Emergency Shutdown) strictly for educational purposes.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9 or higher
- A Google Cloud API Key for Gemini

### 2. Installation
1.  **Clone/Open** this folder.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Setup Environment**:
    - Create a `.env` file in this folder (copy from `.env.example`).
    - Add your API Key:
      ```
      GOOGLE_API_KEY=your_actual_api_key_here
      ```

### 3. Run the App
Double-click `run.bat` (if configured for your system) OR run:
```bash
streamlit run app.py
```

## 🛠️ Project Structure
- `app.py`: Main application code containing the UI, Gemini logic, and Safety Rules.
- `requirements.txt`: List of Python libraries.
- `.env`: (Hidden) Stores your API Key.

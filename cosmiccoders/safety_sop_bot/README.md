# Manufacturing Plant SOP & Safety Explainer Bot

## Project Structure
- `app.py`: Main Streamlit application.
- `requirements.txt`: Python dependencies.
- `.env.example`: Template for the API key.

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
    - Rename `.env.example` to `.env` (or create a `.env` file).
    - Add your Google Gemini API key:
      ```
      GOOGLE_API_KEY=your_actual_api_key_here
      ```
    - Get a key from [Google AI Studio](https://aistudio.google.com/) if you don't have one.

3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Usage
- The app will open in your browser.
- Ask questions like:
  - "Explain lockout–tagout in simple terms"
  - "What safety gear is used near heavy machines?"
  - "Can I skip the safety glasses if I'm just looking?" (Should be refused/corrected)

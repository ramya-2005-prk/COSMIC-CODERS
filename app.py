
import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# --- Configuration & Setup ---
load_dotenv()

# Configure page settings - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="SafePlant AI - SOP Assistant",
    page_icon="🏭",
    layout="centered"
)

# Load API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.warning("⚠️ GOOGLE_API_KEY not found. Please set it in your .env file.")
    if "GOOGLE_API_KEY" not in st.session_state:
        st.session_state["GOOGLE_API_KEY"] = ""

# --- Hardcoded SOP Data (The Knowledge Base) ---
SOP_DATA = """
1. LOCKOUT-TAGOUT (LOTO) PROCEDURE
   - Purpose: Prevent accidental startup of machinery during maintenance.
   - SCOPE: All maintenance personnel working on Class A Heavy Press machines.
   - STEPS:
     1. NOTIFY: Inform affected operators that maintenance is beginning.
     2. SHUTDOWN: Perform normal machine shutdown sequence at the control panel.
     3. ISOLATE: Identify all energy sources (electrical, hydraulic, pneumatic). Turn main disconnect switch to "OFF".
     4. LOCK & TAG: Apply personal padlock and "DANGER - DO NOT OPERATE" tag to the disconnect switch.
     5. RELEASE ENERGY: Bleed off any stored hydraulic pressure; block any movable parts against gravity.
     6. VERIFY (TEST START): Attempt to start the machine to ensure it is dead. Return controls to neutral.
     7. WORK: Perform the scheduled maintenance.
     8. RESTORE: Remove tools, clear personnel, remove lock/tag, and re-energize.

2. PERSONAL PROTECTIVE EQUIPMENT (PPE) - HEAVY MACHINERY ZONE
   - MANDATORY items at all times inside the Yellow Zone:
     - Safety Glasses: ANSI Z87.1 compliant, with side shields.
     - Steel-Toed Boots: ASTM F2413 rated.
     - High-Visibility Vest: Class 2 yellow/green.
     - Hearing Protection: Required if the "High Noise" light is flashing (exceeds 85dB).
   - PROHIBITED items:
     - Loose jewelry, watches, rings.
     - Unbound long hair (must be tied back).
     - Loose sleeves or hoodies with drawstrings.

3. EMERGENCY SHUTDOWN PROCEDURE
   - WHEN TO USE: Fire, chemical spill, severe injury, or machine runaway.
   - STEPS:
     1. ACTIVATE E-STOP: Hit the large RED button on the nearest console immediately.
     2. EVACUATE: Move to the designated "Green Assembly Point" in the parking lot.
     3. DO NOT RESTART: Never attempt to reset the E-Stop until authorized by the Plant Manager.
     4. REPORT: Call the rapid response line (ext 555) once safe.
"""

# --- System Prompt / Behavioral Instructions ---
SYSTEM_PROMPT = f"""
You are the SafePlant AI, a specialized assistant for manufacturing employees.
Your SOLE GOAL is to explain Standard Operating Procedures (SOPs) and safety rules clearly and simply.

CONTEXT DATA:
{SOP_DATA}

STRICT GUIDELINES:
1. EXPLAIN ONLY: Your job is to educate and clarify, not to command.
2. NO APPROVALS: NEVER approve an action, permit, or risk assessment. If a user asks "Can I do X?", say "I cannot approve actions. Please check with your supervisor."
3. NO OPERATION: Do not give real-time operational commands like "Press the button now." Instead say "The SOP states strict steps..."
4. NEUTRAL TONE: Be helpful, professional, and serious about safety. Use simple English suitable for new hires.
5. SOURCE OF TRUTH: Answer ONLY based on the provided SOP sections (LOTO, PPE, Emergency). If it's not in the text, say "I don't have information on that specific protocol."

If the user asks for a decision (e.g., "Is this safe to run?"), REJECT it and REFER to a human supervisor.
"""

# --- App UI & Logic ---

# Custom CSS for the safety banner and polish
st.markdown("""
    <style>
    .safety-banner {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeeba;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: bold;
    }
    .stChatMessage {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🏭 SafePlant AI")
st.markdown("### Manufacturing SOP & Safety Explainer")

# Safety Banner
st.markdown('<div class="safety-banner">⚠️ DISCLAIMER: This AI explains SOPs for educational purposes only. It DOES NOT replace supervisors, safety officers, or official training. For approvals, contact your lead.</div>', unsafe_allow_html=True)

# Sidebar with context
with st.sidebar:
    st.header("📝 Available SOPs")
    st.markdown("- **Lockout-Tagout (LOTO)**")
    st.markdown("- **PPE Requirements** (Heavy Machinery)")
    st.markdown("- **Emergency Shutdown**")
    st.markdown("---")
    st.info("💡 **Tip:** Ask questions like 'What PPE do I need?' or 'Explain LOTO steps'.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add an initial greeting from the AI
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I can explain the LOTO procedures, PPE requirements, and Emergency Shutdown rules. What would you like to know?"
    })

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about procedures..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    if not api_key:
        st.error("API Key is missing. Cannot generate response.")
    else:
        try:
            with st.spinner("Analyzing safety protocols..."):
                client = genai.Client(api_key=api_key)
                
                # Create history for Gemini
                history_for_gemini = []
                for m in st.session_state.messages:
                    if m["content"] == "Hello! I can explain the LOTO procedures, PPE requirements, and Emergency Shutdown rules. What would you like to know?":
                        continue
                    
                    role = "model" if m["role"] == "assistant" else "user"
                    history_for_gemini.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))
                
                # Add the current prompt
                history_for_gemini.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=history_for_gemini,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )
                )
                
                if response.text:
                    bot_reply = response.text
                else:
                    bot_reply = "I apologize, but I couldn't generate a clear answer. Please verify the question."

            # Display and save assistant response
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(bot_reply)

        except Exception as e:
            st.error(f"System Error: {str(e)}")

import os
import openai

def interpret_command(text):
    # Load your OpenAI key from environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable")

    client = openai.OpenAI()

    # Send the text to GPT and get a structured command as response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
             """You are JARVIS, an intelligent personal assistant. 
Always respond with valid JSON, using only the format specified. 
If the user's command includes multiple actions (e.g., both save a note and set a reminder), 
respond as a JSON array: each object must contain a single action according to the spec below.

Response Format for one action:
{
  "action": "<action_type>",
  "content": "<extracted_content>",
  "metadata": {
    "timestamp": "<current_timestamp>",
    "intent": "<user_intent>",
    "priority": "<low|medium|high>",
    "category": "<work|personal|reminder|task>",
    "keywords": ["<keyword1>", "<keyword2>"]
  }
}

For multiple actions, respond as an array:
[
  { /* note object */ },
  { /* reminder object */ }
]

Action Types:
1. NOTE_CREATE - When user wants to save information
2. REMINDER_CREATE - When user wants to set a reminder
3. NOTE_RETRIEVE - When user wants to recall notes
4. REMINDER_RETRIEVE - When user wants to recall reminders

Context Rules:
- Extract keywords for better searchability
- Detect time references: "today", "tomorrow" = high priority; "sometime", "later" = low priority
- Identify and split separate requests if present
- Only output valid JSON, with no commentary, no markdown, and no explanations.
- If the user's command mixes a note and a reminder, output both in the correct array format.
"""
            },
            {"role": "user", "content": text}
        ],
    )

    # Parse and return the response text (which should be a JSON string or a JSON array string)
    return response.choices[0].message.content

import os
import openai

def interpret_command(text):
    # Load your OpenAI key from environment variable
    openai.api_key = os.getenv("OpenAI_API_key")
    if not openai.api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable")

    client = openai.OpenAI()

    # Send the text to GPT and get a structured command as response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
             """(You are JARVIS, an intelligent personal assistant. Respond with valid JSON only)

Response Format:
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

Action Types:

1. NOTE_CREATE - When user wants to save information
   Triggers: "note this down", "remember this", "take note", "jot this down"
   Extract the actual content without command phrases
   Identify action items and urgency
   Example: "Take note that I have to work on my startup codebase today"
   Output: {"action": "NOTE_CREATE", "content": "Work on startup codebase", "metadata": {"intent": "task_reminder", "priority": "high", "category": "work", "keywords": ["startup", "codebase", "today"]}}

2. NOTE_RETRIEVE - When user wants to recall notes
   Triggers: "what did I ask you to note", "what did I tell you", "remind me what"
   Extract search parameters from the query
   Example: "What did I ask you to note about my startup?"
   Output: {"action": "NOTE_RETRIEVE", "content": "Query notes related to startup", "metadata": {"intent": "recall_request", "keywords": ["startup"]}}

Context Rules:
- Extract keywords for better searchability
- Detect time references: "today", "tomorrow" = high priority; "sometime", "later" = low priority
- Identify action verbs: "work on", "finish", "complete", "call"
- If unclear, default to INFO_REQUEST

Always output valid JSON. Be concise and extract actionable information."""
            },
            {"role": "user", "content": text}
        ],
    )

    # Parse and return the response text (which should be a JSON string)
    return response.choices[0].message.content

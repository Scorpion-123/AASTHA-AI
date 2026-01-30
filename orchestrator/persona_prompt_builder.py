#-------------------------Lambda Function-------------------------------------
    #Input: {"consumer_name": "Abhishek", "category": "STANDARD"}
    #output: {"category": "STANDARD", "persona_prompt": "<FULL PROMPT HERE>"}
#-----------------------------------------------------------------------------

import json

# =====================================================
# ✅ PERSONA PROMPTS (Style Packs)
# =====================================================

STANDARD_PROMPT = """
You are Aastha, the official virtual assistant of CESC Ltd.

You must respond using CESC’s Standard Communication Style
(as used in official SMS, safety alerts, and customer support messages).

=============================
CESC STANDARD WRITING STYLE
=============================

Tone and Language Rules:
- Always sound like an official electricity utility communication.
- Be formal, clear, professional, and safety-focused.
- Do NOT use casual tone, slang, emojis, or jokes.
- Use short and direct sentences.

Personalization Rules:
- If the consumer name is available, start with:
  "Dear <ConsumerName>,"
- If not available, start with:
  "Dear Consumer,"

Format Rules:
- Responses must be concise (maximum 3–4 lines).
- Use strong alert wording when required:
  "URGENT:", "Never touch...", "Please stay safe..."
- If escalation is needed, include:
  "For any assistance call 1912."
- If a link or dynamic value is required, use placeholder:
  {#var#}
- End every response with:
  "- CESC Ltd."

Guardrails:
- Do NOT invent policies, compensation, or unsafe electrical advice.
- If unsure, Ask follow-ups to the user to know their intent or reference the knowleadgebase (if available).

=============================
STYLE EXAMPLES
=============================

Example:
Dear Consumer, please stay safe in the rain and follow our safety tips provided below {#var#} - CESC Ltd.

Example:
Never touch an electrical pole/ hanging wire/ pillar-box during and after heavy rain.
For any assistance call 1912 - CESC Ltd.

=============================
Always respond in this style.
"""

# Placeholder prompts for future categories
GENZ_PROMPT = """
[GENZ STYLE PROMPT NOT YET PROVIDED]
"""

MILLENNIAL_PROMPT = """
[MILLENNIAL STYLE PROMPT NOT YET PROVIDED]
"""

BOOMER_PROMPT = """
[BOOMER STYLE PROMPT NOT YET PROVIDED]
"""

# =====================================================
# ✅ Category Mapping
# =====================================================

STYLE_PROMPTS = {
    "STANDARD": STANDARD_PROMPT,
    "GENZ": GENZ_PROMPT,
    "MILLENNIAL": MILLENNIAL_PROMPT,
    "BOOMER": BOOMER_PROMPT
}


# =====================================================
# ✅ Lambda Handler
# =====================================================

def lambda_handler(event, context):
    """
    Expected Input:
    {
        "consumer_name": "Abhishek",
        "category": "STANDARD"
    }
    """

    # Extract inputs
    consumer_name = event.get("consumer_name", None)
    category = event.get("category", "STANDARD").upper()

    # Validate category
    if category not in STYLE_PROMPTS:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Invalid category '{category}'. Supported: {list(STYLE_PROMPTS.keys())}"
            })
        }

    # Get base prompt
    persona_prompt = STYLE_PROMPTS[category]

    # Add consumer personalization hint
    if consumer_name:
        greeting_rule = f'Remember: Start responses with "Dear {consumer_name},"'
    else:
        greeting_rule = 'Remember: Start responses with "Dear Consumer,"'

    final_prompt = persona_prompt + "\n\n" + greeting_rule

    # Return persona prompt
    return {
        "statusCode": 200,
        "body": json.dumps({
            "category": category,
            "persona_prompt": final_prompt
        })
    }

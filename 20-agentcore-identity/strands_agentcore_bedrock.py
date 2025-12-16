from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

# PTO data
PTO_HOURS_AVAILABLE = 94


# Define tools using @tools decorator
@tool
def get_available_pto_hours() -> str:
    """Get the total number of PTO hours available."""
    return f"You have {PTO_HOURS_AVAILABLE} PTO hours available."

@tool
def get_available_pto_days() -> str:
    """Convert PTO hours to days (assuming 8-hour workday)."""
    days = PTO_HOURS_AVAILABLE / 8
    return f"You have {days} PTO days available ({PTO_HOURS_AVAILABLE} hours)."

@tool
def can_take_full_day() -> str:
    """Check if employee has enough PTO for a full day off (8 hours)."""
    if PTO_HOURS_AVAILABLE >= 8:
        return f"Yes, you can take a full day off. You have {PTO_HOURS_AVAILABLE} hours available."
    else:
        return f"No, you don't have enough PTO for a full day. You only have {PTO_HOURS_AVAILABLE} hours available."

@tool
def can_take_half_day() -> str:
    """Check if employee has enough PTO for a half day off (4 hours)."""
    if PTO_HOURS_AVAILABLE >= 4:
        return f"Yes, you can take a half day off. You have {PTO_HOURS_AVAILABLE} hours available."
    else:
        return f"No, you don't have enough PTO for a half day. You only have {PTO_HOURS_AVAILABLE} hours available."


# Initialize model
model = BedrockModel(model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0")


# Create agent
agent = Agent(
    model=model,
    system_prompt="You are a helpful HR assistant that helps employees check their PTO (Paid Time Off) hours. Be friendly, concise, and professional.",
    tools=[get_available_pto_hours, get_available_pto_days, can_take_full_day, can_take_half_day]
)

@app.entrypoint
def strands_bedrock_agentcore(payload):
    """Invoke the agent with a payload"""
    user_input = payload.get("prompt")
    response = agent(user_input)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()

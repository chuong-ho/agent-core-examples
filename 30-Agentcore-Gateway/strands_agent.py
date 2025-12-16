from strands import Agent, tool
import argparse
import json
from strands.models import BedrockModel
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
import boto3
from datetime import datetime

# Load environment variables
load_dotenv()



# Check AWS credentials and boto sessions 


# PTO data
PTO_HOURS_AVAILABLE = 94

try:
    # Create a Bedrock client to test credentials
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-1')

    # Try to get caller identity to verify credentials
    sts = boto3.client('sts', region_name='us-west-2')
    identity = sts.get_caller_identity()



    # If using temporary credentials, check expiration
    session = boto3.Session()
    credentials = session.get_credentials()


except Exception as e:
    print(f"❌ AWS Credentials Error: {e}")
    print("\n🔧 To fix this:")
    print("   1. Run: aws configure")
    print("   2. Or update your .env file with new AWS credentials")
    print("   3. Or get fresh credentials from AWS SSO/Academy")
    print("\n   Then restart the kernel and run from the beginning.")


# Define tools using if-else logic with the @tool decorator
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


try:
    model = BedrockModel(
        model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        boto_session=session
    )

except Exception as e:
    print(f"⚠️  Error initializing Bedrock model: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Check AWS credentials are valid (run cell 5)")
    print("2. Enable Claude Sonnet 4 in Bedrock console → Model access")
    print("3. Use inference profile (us.anthropic.claude-sonnet-4-v1:0)")
    print("4. Try different region if needed (us-east-1, us-west-2)")


# Define the system prompt for the PTO agent
system_prompt = """You are a helpful HR assistant that helps employees check their PTO (Paid Time Off) hours. 
Be friendly, concise, and professional. Use the available tools to provide accurate information about PTO balances."""

# Create the PTO agent with tools
pto_agent = Agent(
    model=model,
    system_prompt=system_prompt,
    tools=[
        get_available_pto_hours,
        get_available_pto_days,
        can_take_full_day,
        can_take_half_day
    ]
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=str)
    args = parser.parse_args()
    payload = json.loads(args.payload)
    response = pto_agent(payload.get("prompt"))
    print(response.message['content'][0]['text'])

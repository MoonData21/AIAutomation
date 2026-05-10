import json
import anthropic
from loguru import logger
from app.core.config import settings
from app.utils.retry import llm_retry

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are an expert financial analyst and stock market strategist.
You always respond with valid JSON only — no markdown, no explanation, just raw JSON.
"""


@llm_retry
def call_claude(prompt: str, max_tokens: int = 1024) -> dict:
    """Call Claude and return parsed JSON response."""
    logger.debug(f"Calling Claude: {prompt[:80]}...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude response as JSON: {raw}")
        raise ValueError(f"Claude returned invalid JSON: {e}")
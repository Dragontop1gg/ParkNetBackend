import json
import logging
import re
from typing import Any

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def analyze_report(category: str, description: str) -> dict[str, Any] | None:
    """
    Call OpenRouter to classify priority and summarize. Returns dict with keys:
    priority (1-5), confirmed_category, summary (short text).
    """
    api_key = getattr(settings, "OPENROUTER_API_KEY", "") or ""
    if not api_key.strip():
        return None

    model = getattr(
        settings,
        "OPENROUTER_MODEL",
        "google/gemma-2-9b-it:free",
    )

    system = (
        "You are an expert urban park operations analyst. "
        "Analyze the citizen report and respond with ONLY valid JSON (no markdown). "
        "Keys: "
        "priority (integer 1-5, where 1=Low, 3=Medium, 5=Critical/Safety Hazard), "
        "priority_label (string: Low, Medium, High, or Critical), "
        "confirmed_category (string, one of: littering, vandalism, broken_path, safety, lighting, other), "
        "summary (one concise, professional sentence for maintenance crews)."
    )
    user_msg = f"Report category (user-selected): {category}\nDescription: {description or 'N/A'}"

    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.2,
            },
            timeout=45,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except Exception as exc:
        logger.exception("OpenRouter request failed: %s", exc)
        return None

    parsed = _parse_json_content(content)
    if not parsed:
        return {"raw_text": content, "parse_error": True}

    out: dict[str, Any] = {}
    if "priority" in parsed:
        try:
            p = int(parsed["priority"])
            out["priority"] = max(1, min(5, p))
        except (TypeError, ValueError):
            out["priority"] = 3
    else:
        out["priority"] = 3

    out["confirmed_category"] = str(parsed.get("confirmed_category", category))
    out["summary"] = str(parsed.get("summary", ""))[:500]
    return out


def _parse_json_content(content: str) -> dict[str, Any] | None:
    content = content.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
    if fence:
        content = fence.group(1).strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{[\s\S]*\}", content)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    return None

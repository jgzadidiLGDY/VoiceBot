from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from openai import OpenAI


def build_bug_analysis_prompt(
    *,
    scenario: dict,
    transcript: str,
    call_id: str,
    duration_ms: int | None,
) -> str:
    return f"""
You are reviewing a bot-to-bot healthcare office call for useful bug findings.

Your job:
- Identify only meaningful issues.
- Ignore tiny transcription glitches and minor wording oddities.
- Prefer useful bugs over nitpicks.
- If there is no meaningful bug, say so clearly.

Scenario metadata:
{json.dumps(scenario, indent=2)}

Call metadata:
- call_id: {call_id}
- duration_ms: {duration_ms}

Transcript:
\"\"\"
{transcript}
\"\"\"

Return strict JSON with this schema:
{{
  "summary": "short overall assessment",
  "has_meaningful_bug": true,
  "bugs": [
    {{
      "title": "short bug title",
      "severity": "low|medium|high",
      "category": "clarification|consistency|workflow|factual|transfer|other",
      "description": "what happened",
      "why_it_matters": "why this is a real issue",
      "transcript_evidence": "quote or short excerpt",
      "suggested_fix": "practical suggestion"
    }}
  ],
  "strengths": [
    "short note"
  ]
}}

Rules:
- At most 3 bugs.
- If no meaningful bug exists, return:
  - has_meaningful_bug = false
  - bugs = []
- Use the scenario fields stress_target, success_condition, and good_bug_signals to guide evaluation.
""".strip()


def analyze_transcript_with_llm(
    *,
    openai_api_key: str,
    model: str,
    scenario: dict,
    transcript: str,
    call_id: str,
    duration_ms: int | None,
) -> dict[str, Any]:
    client = OpenAI(api_key=openai_api_key)

    prompt = build_bug_analysis_prompt(
        scenario=scenario,
        transcript=transcript,
        call_id=call_id,
        duration_ms=duration_ms,
    )

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    text = response.output_text.strip()
    return json.loads(text)


def save_bug_analysis(
    *,
    output_dir: str,
    call_id: str,
    analysis: dict[str, Any],
) -> str:
    bug_dir = Path(output_dir) / "bug_analysis"
    bug_dir.mkdir(parents=True, exist_ok=True)

    path = bug_dir / f"{call_id}_bug_analysis.json"
    path.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)
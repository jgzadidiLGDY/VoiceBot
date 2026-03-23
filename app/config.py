from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    retell_api_key: str
    retell_from_number: str
    retell_to_number: str
    retell_agent_id: str | None
    poll_interval_seconds: int
    max_wait_seconds: int
    output_dir: str

    openai_api_key: str | None
    enable_bug_analysis: bool
    openai_model: str

    @staticmethod
    def from_env() -> "Settings":
        api_key = os.getenv("RETELL_API_KEY", "").strip()
        from_number = os.getenv("RETELL_FROM_NUMBER", "").strip()
        to_number = os.getenv("RETELL_TO_NUMBER", "").strip()
        agent_id = os.getenv("RETELL_AGENT_ID", "").strip() or None

        if not api_key:
            raise ValueError("RETELL_API_KEY is required.")
        if not from_number:
            raise ValueError("RETELL_FROM_NUMBER is required.")
        if not to_number:
            raise ValueError("RETELL_TO_NUMBER is required.")

        enable_bug_analysis = os.getenv("ENABLE_BUG_ANALYSIS", "true").strip().lower() in {
            "1", "true", "yes", "on"
        }

        openai_api_key = os.getenv("OPENAI_API_KEY", "").strip() or None

        return Settings(
            retell_api_key=api_key,
            retell_from_number=from_number,
            retell_to_number=to_number,
            retell_agent_id=agent_id,
            poll_interval_seconds=int(os.getenv("POLL_INTERVAL_SECONDS", "5")),
            max_wait_seconds=int(os.getenv("MAX_WAIT_SECONDS", "300")),
            output_dir=os.getenv("OUTPUT_DIR", "outputs").strip() or "outputs",
            openai_api_key=openai_api_key,
            enable_bug_analysis=enable_bug_analysis,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1").strip() or "gpt-4.1",
        )
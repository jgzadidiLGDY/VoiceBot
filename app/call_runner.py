from __future__ import annotations

import time
from datetime import datetime, timezone

from app.artifact_capture import save_call_artifacts
from app.bug_analyzer import analyze_transcript_with_llm, save_bug_analysis
from app.config import Settings
from app.retell_api import RetellAPI
from app.scenarios import get_default_scenario, get_scenario_by_id, scenario_to_dynamic_vars


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def wait_for_call_completion(
    *,
    client: RetellAPI,
    call_id: str,
    poll_interval_seconds: int,
    max_wait_seconds: int,
) -> dict:
    started = time.time()

    while True:
        call_data = client.get_call(call_id)

        if call_data.get("end_timestamp"):
            return call_data

        elapsed = time.time() - started
        if elapsed >= max_wait_seconds:
            raise TimeoutError(
                f"Timed out waiting for call {call_id} to finish after {max_wait_seconds} seconds."
            )

        print(
            f"[poll] call_id={call_id} elapsed={int(elapsed)}s "
            f"status=waiting_for_end"
        )
        time.sleep(poll_interval_seconds)


def maybe_run_bug_analysis(
    *,
    settings: Settings,
    scenario: dict,
    call_id: str,
    final_call_data: dict,
) -> str | None:
    if not settings.enable_bug_analysis:
        return None

    if not settings.openai_api_key:
        print("[bug-analysis] skipped: OPENAI_API_KEY not set")
        return None

    transcript = final_call_data.get("transcript") or ""
    if not transcript.strip():
        print("[bug-analysis] skipped: transcript missing")
        return None

    print("[bug-analysis] analyzing transcript with LLM...")
    analysis = analyze_transcript_with_llm(
        openai_api_key=settings.openai_api_key,
        model=settings.openai_model,
        scenario=scenario,
        transcript=transcript,
        call_id=call_id,
        duration_ms=final_call_data.get("duration_ms"),
    )
    return save_bug_analysis(
        output_dir=settings.output_dir,
        call_id=call_id,
        analysis=analysis,
    )


def run_call_for_scenario(settings: Settings, scenario: dict) -> dict:
    dynamic_vars = scenario_to_dynamic_vars(scenario)

    metadata = {
        "project_stage": "stage_4",
        "scenario_id": scenario["scenario_id"],
        "scenario_title": scenario["title"],
        "started_at_utc": utc_now_iso(),
    }

    client = RetellAPI(settings.retell_api_key)

    print("[start] creating outbound call...")
    create_resp = client.create_phone_call(
        from_number=settings.retell_from_number,
        to_number=settings.retell_to_number,
        metadata=metadata,
        retell_llm_dynamic_variables=dynamic_vars,
        override_agent_id=settings.retell_agent_id,
    )

    call_id = create_resp.get("call_id")
    if not call_id:
        raise RuntimeError(f"No call_id returned from Retell: {create_resp}")

    print(f"[start] call created: {call_id}")
    print(f"[info] scenario_id={scenario['scenario_id']}")
    print("[wait] polling until call ends...")

    final_call_data = wait_for_call_completion(
        client=client,
        call_id=call_id,
        poll_interval_seconds=settings.poll_interval_seconds,
        max_wait_seconds=settings.max_wait_seconds,
    )

    print("[done] call ended, saving artifacts...")
    saved = save_call_artifacts(
        output_dir=settings.output_dir,
        call_id=call_id,
        call_data=final_call_data,
        scenario=scenario,
    )

    bug_analysis_path = maybe_run_bug_analysis(
        settings=settings,
        scenario=scenario,
        call_id=call_id,
        final_call_data=final_call_data,
    )

    result = {
        "call_id": call_id,
        "scenario_id": scenario["scenario_id"],
        "duration_ms": final_call_data.get("duration_ms"),
        "transcript_available": bool(final_call_data.get("transcript")),
        "recording_url_available": bool(
            final_call_data.get("recording_url")
            or final_call_data.get("scrubbed_recording_url")
            or final_call_data.get("recording_multi_channel_url")
            or final_call_data.get("scrubbed_recording_multi_channel_url")
        ),
        "saved": saved,
        "bug_analysis_path": bug_analysis_path,
    }
    return result


def run_default_call(settings: Settings) -> dict:
    scenario = get_default_scenario()
    return run_call_for_scenario(settings, scenario)


def run_call_by_scenario_id(settings: Settings, scenario_id: str) -> dict:
    scenario = get_scenario_by_id(scenario_id)
    return run_call_for_scenario(settings, scenario)
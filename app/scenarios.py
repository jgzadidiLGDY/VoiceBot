from __future__ import annotations


def get_stage3_scenarios() -> list[dict]:
    return [
        {
            "scenario_id": "schedule_new_patient",
            "title": "New patient appointment scheduling",
            "category": "scheduling",
            "scenario_type": "normal",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "polite",
            },
            "goal": "Schedule a routine primary care appointment for next week, preferably a weekday morning.",
            "known_facts": {
                "preferred_day_window": "next week",
                "preferred_time": "weekday morning",
                "is_new_patient": "yes",
            },
            "behavior_style": ["polite", "straightforward"],
            "stress_target": "basic_flow",
            "must_try": [
                "Ask for the next available weekday morning appointment."
            ],
            "success_condition": "A natural appointment discussion occurs and the call ends coherently after options or next steps are discussed.",
            "good_bug_signals": [
                "The agent becomes incoherent.",
                "The agent confirms an appointment without enough information.",
                "The agent fails to handle a basic scheduling flow.",
            ],
        },
        {
            "scenario_id": "reschedule_existing_appointment",
            "title": "Reschedule an existing appointment",
            "category": "reschedule",
            "scenario_type": "normal",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "polite",
            },
            "goal": "Reschedule an existing appointment to next week, preferably a weekday morning.",
            "known_facts": {
                "has_existing_appointment": "yes",
                "current_appointment_time": "this Friday at 2:00 PM",
                "preferred_day_window": "next week",
                "preferred_time": "weekday morning",
            },
            "behavior_style": ["polite", "slightly_rushed"],
            "stress_target": "context_change",
            "must_try": [
                "Say you already have an appointment but need to move it.",
                "Ask for weekday morning options next week."
            ],
            "success_condition": "The agent understands the change request and discusses alternative appointment times.",
            "good_bug_signals": [
                "The agent ignores that there is already an appointment.",
                "The agent restarts the booking flow incorrectly.",
                "The agent gives contradictory rescheduling instructions.",
            ],
        },
        {
            "scenario_id": "cancel_existing_appointment",
            "title": "Cancel an existing appointment",
            "category": "cancel",
            "scenario_type": "normal",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "brief",
            },
            "goal": "Cancel an upcoming appointment and confirm whether it has been canceled.",
            "known_facts": {
                "has_existing_appointment": "yes",
                "current_appointment_time": "next Tuesday at 10:30 AM",
            },
            "behavior_style": ["brief", "polite"],
            "stress_target": "confirmation_logic",
            "must_try": [
                "Say you need to cancel an upcoming appointment.",
                "Ask for confirmation that the cancellation is complete."
            ],
            "success_condition": "The cancellation request is handled clearly and the call ends naturally.",
            "good_bug_signals": [
                "The agent fails to confirm the cancellation outcome.",
                "The agent redirects into scheduling without handling cancellation first.",
                "The agent becomes unclear about whether the appointment still exists.",
            ],
        },
        {
            "scenario_id": "office_hours_weekend",
            "title": "Ask about weekend office hours",
            "category": "office_hours",
            "scenario_type": "normal",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "polite",
            },
            "goal": "Find out whether the office is open on Saturday morning and what the weekday hours are.",
            "known_facts": {
                "requested_day": "Saturday",
                "requested_time": "morning",
            },
            "behavior_style": ["polite", "slightly_confused"],
            "stress_target": "factual_correctness",
            "must_try": [
                "Ask whether the office is open on Saturday morning.",
                "If needed, ask what the weekday hours are instead."
            ],
            "success_condition": "The agent gives a clear answer about office availability and hours.",
            "good_bug_signals": [
                "The agent gives contradictory office-hour information.",
                "The agent avoids answering the direct office-hours question.",
                "The agent confidently provides incorrect availability.",
            ],
        },
        {
            "scenario_id": "insurance_acceptance_aetna",
            "title": "Ask whether Aetna PPO is accepted",
            "category": "insurance",
            "scenario_type": "normal",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "careful",
            },
            "goal": "Find out whether Aetna PPO is accepted before scheduling an appointment.",
            "known_facts": {
                "insurance_plan": "Aetna PPO",
                "intent_before_booking": "verify insurance first",
            },
            "behavior_style": ["polite", "careful"],
            "stress_target": "policy_consistency",
            "must_try": [
                "Ask directly whether Aetna PPO is accepted.",
                "Ask what you should do if coverage needs to be verified."
            ],
            "success_condition": "The agent answers the insurance question clearly or explains the next step for verification.",
            "good_bug_signals": [
                "The agent gives an overconfident insurance answer without caveats.",
                "The agent contradicts itself about insurance acceptance.",
                "The agent fails to explain what to do next if unsure.",
            ],
        },
        {
            "scenario_id": "medication_refill_lisinopril",
            "title": "Request a refill for Lisinopril",
            "category": "refill",
            "scenario_type": "normal",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "calm",
            },
            "goal": "Ask how to request a refill for Lisinopril and what information is needed.",
            "known_facts": {
                "medication_name": "Lisinopril",
                "is_existing_medication": "yes",
            },
            "behavior_style": ["calm", "direct"],
            "stress_target": "process_explanation",
            "must_try": [
                "Ask whether you can request a refill for Lisinopril.",
                "Ask what information the office needs to process the refill."
            ],
            "success_condition": "The agent gives a coherent refill process or next-step explanation.",
            "good_bug_signals": [
                "The agent gives unclear refill instructions.",
                "The agent skips needed clarification entirely.",
                "The agent sounds unsafe or overly confident about refill handling.",
            ],
        },
        {
            "scenario_id": "location_question",
            "title": "Ask which office location to visit",
            "category": "location",
            "scenario_type": "normal",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "polite",
            },
            "goal": "Find out which office location is best and ask for the address.",
            "known_facts": {
                "location_uncertainty": "yes",
                "preference": "closest office if multiple locations exist",
            },
            "behavior_style": ["polite", "slightly_confused"],
            "stress_target": "disambiguation",
            "must_try": [
                "Ask which location you should go to.",
                "Ask for the address if multiple locations exist."
            ],
            "success_condition": "The agent provides location guidance or asks clarifying questions about which office is appropriate.",
            "good_bug_signals": [
                "The agent assumes a location without enough information.",
                "The agent gives conflicting location details.",
                "The agent fails to provide useful address guidance.",
            ],
        },
    ]


def get_stage4_scenarios() -> list[dict]:
    return [
        {
            "scenario_id": "ambiguous_appointment_request",
            "title": "Ambiguous request for an appointment",
            "category": "ambiguity",
            "scenario_type": "edge_case",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "uncertain",
            },
            "goal": "Ask for an appointment in a vague way and wait for the office to clarify what kind of visit is needed.",
            "known_facts": {
                "wants_appointment": "yes",
                "specific_visit_type_known": "no",
                "specific_time_known": "no",
            },
            "behavior_style": ["polite", "uncertain", "under_specified"],
            "stress_target": "clarification_quality",
            "must_try": [
                "Say you need to come in sometime soon but are not sure exactly what kind of appointment to ask for.",
                "Only provide more detail after the office asks clarifying questions."
            ],
            "success_condition": "The office asks useful follow-up questions instead of guessing too early.",
            "good_bug_signals": [
                "The agent assumes a visit type without enough information.",
                "The agent gives irrelevant scheduling options before clarifying the request.",
                "The agent loops without narrowing the request.",
            ],
        },
        {
            "scenario_id": "interrupting_patient_scheduling",
            "title": "Scheduling with mild interruption",
            "category": "interruption",
            "scenario_type": "edge_case",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "mildly_impatient",
            },
            "goal": "Schedule a new patient appointment while interrupting once or twice naturally if the office gives long explanations.",
            "known_facts": {
                "is_new_patient": "yes",
                "preferred_day_window": "next week",
                "preferred_time": "weekday morning",
            },
            "behavior_style": ["polite", "mildly_impatient", "interrupts_once_or_twice"],
            "stress_target": "interruption_recovery",
            "must_try": [
                "If the office gives a long explanation, cut in once with a direct scheduling question.",
                "Keep the interruption natural and brief."
            ],
            "success_condition": "The conversation remains coherent and the office recovers from interruption without losing the task.",
            "good_bug_signals": [
                "The agent restarts or loops after interruption.",
                "The agent ignores the interruption and continues off-topic.",
                "The agent becomes incoherent after turn-taking overlap.",
            ],
        },
        {
            "scenario_id": "changes_mind_mid_call",
            "title": "Patient changes mind mid-call",
            "category": "workflow_shift",
            "scenario_type": "edge_case",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "indecisive",
            },
            "goal": "Start by asking to reschedule an appointment, then decide during the call that cancellation would be better.",
            "known_facts": {
                "has_existing_appointment": "yes",
                "current_appointment_time": "this Friday at 2:00 PM",
            },
            "behavior_style": ["polite", "indecisive", "changes_mind_midway"],
            "stress_target": "context_switching",
            "must_try": [
                "Begin by asking to reschedule an existing appointment.",
                "After options are discussed, say it would be better to cancel instead."
            ],
            "success_condition": "The office pivots from rescheduling to cancellation without confusion or contradiction.",
            "good_bug_signals": [
                "The agent stays stuck in the original rescheduling flow.",
                "The agent confirms both cancellation and rescheduling inconsistently.",
                "The agent loses track of which appointment action is active.",
            ],
        },
        {
            "scenario_id": "contradictory_availability_preference",
            "title": "Patient changes availability preference",
            "category": "preference_shift",
            "scenario_type": "edge_case",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "polite",
            },
            "goal": "Ask for a weekday morning appointment, then after options are offered say that afternoon may actually work better.",
            "known_facts": {
                "is_new_patient": "yes",
                "initial_preference": "weekday morning",
                "revised_preference": "weekday afternoon",
            },
            "behavior_style": ["polite", "flexible", "changes_preference_once"],
            "stress_target": "constraint_update_handling",
            "must_try": [
                "First ask for weekday morning options.",
                "After hearing options, revise your preference and ask about afternoon availability instead."
            ],
            "success_condition": "The office adapts to the revised preference without confusion.",
            "good_bug_signals": [
                "The agent ignores the updated preference.",
                "The agent keeps offering old options after the constraint changed.",
                "The agent becomes contradictory about available times.",
            ],
        },
        {
            "scenario_id": "weekend_booking_pushback",
            "title": "Polite pushback on unavailable weekend booking",
            "category": "factual_trap",
            "scenario_type": "adversarial_light",
            "patient_profile": {
                "name": "Maria Lopez",
                "age_band": "adult",
                "tone": "polite_persistent",
            },
            "goal": "Ask whether an appointment can be booked for Sunday morning, and politely ask for confirmation once if told no.",
            "known_facts": {
                "requested_day": "Sunday",
                "requested_time": "morning",
                "persistence_level": "light",
            },
            "behavior_style": ["polite", "persistent_once", "calm"],
            "stress_target": "factual_consistency",
            "must_try": [
                "Ask whether Sunday morning booking is possible.",
                "If told no, politely ask once more whether there is any exception or any Sunday availability at all."
            ],
            "success_condition": "The office consistently refuses invalid weekend scheduling if that is the policy, and offers a valid alternative.",
            "good_bug_signals": [
                "The agent incorrectly confirms weekend availability.",
                "The agent contradicts its own office-hours policy.",
                "The agent offers invalid appointment times after refusing them.",
            ],
        },
    ]


def get_all_scenarios() -> list[dict]:
    return get_stage3_scenarios() + get_stage4_scenarios()


def get_scenario_by_id(scenario_id: str) -> dict:
    for scenario in get_all_scenarios():
        if scenario["scenario_id"] == scenario_id:
            return scenario
    raise ValueError(f"Unknown scenario_id: {scenario_id}")


def get_default_scenario() -> dict:
    return get_scenario_by_id("schedule_new_patient")


def scenario_to_dynamic_vars(scenario: dict) -> dict[str, str]:
    profile = scenario["patient_profile"]
    known_facts = scenario["known_facts"]

    known_facts_str = "; ".join(f"{k}={v}" for k, v in known_facts.items())
    behavior_style_str = ", ".join(scenario["behavior_style"])
    must_try_str = " | ".join(scenario["must_try"])

    return {
        "scenario_id": str(scenario["scenario_id"]),
        "title": str(scenario["title"]),
        "category": str(scenario["category"]),
        "scenario_type": str(scenario["scenario_type"]),
        "patient_name": str(profile["name"]),
        "age_band": str(profile["age_band"]),
        "tone": str(profile["tone"]),
        "goal": str(scenario["goal"]),
        "known_facts": known_facts_str,
        "behavior_style": behavior_style_str,
        "stress_target": str(scenario["stress_target"]),
        "must_try": must_try_str,
        "success_condition": str(scenario["success_condition"]),
    }
# Bug Report — Patient Voice (QA) Bot

## Bug Discovery Approach

To identify issues, I used a hybrid workflow:

1. Executed multiple realistic outbound calls across healthcare scenarios.
2. Used an AI-assisted script to perform a first-pass scan of transcripts.
3. Manually reviewed recordings and transcripts to confirm severity and remove false positives.

This approach helped efficiently surface meaningful workflow and data-handling issues.

---

## Bug 1 — Workflow Cannot Pivot from Rescheduling to Cancellation

**Severity:** High

**Call:** `call_fb5a9220f5a469f4694bda9b948.txt`

**Description:**
During a rescheduling request, the system encountered difficulty retrieving available appointment slots. Instead of confirming whether the patient wanted to continue rescheduling or take another action (such as cancelling the appointment), the agent immediately attempted to transfer the call. This prevented testing of the intended mid-call intent change.

**Transcript Evidence:**
User: “I'm having trouble accessing the available times to reschedule your appointment. I'll connect you to our clinic support team…”

**Why It’s a Problem:**
Patients frequently change their minds mid-call. The agent should explicitly confirm updated intent before escalation. Failing to do so can leave requests unresolved and increase operational call load.

---

## Bug 2 — Appointment Record Mismatch Not Clarified

**Severity:** Medium

**Call:** `call_7ca38399606434eee2662275de0.txt`

**Description:**
The patient requested cancellation of an appointment scheduled for “next Tuesday at 10:30 AM,” but the system listed only Thursday and Friday appointments. The agent proceeded to confirm cancellation of a Thursday appointment without clarifying the discrepancy.

**Transcript Evidence:**
Agent: “I need to cancel my upcoming appointment that’s scheduled for next Tuesday at 10:30 AM.”
User: “You have two upcoming appointments… one on Thursday… another on Friday…”

**Why It’s a Problem:**
Mismatch between patient-reported information and system records can lead to incorrect appointment changes. The agent should verify whether the patient may have mistaken the date or escalate the discrepancy.

---

## Bug 3 — Provider Name Inconsistency During Appointment Confirmation

**Severity:** Medium

**Call:** `call_baa1a8ddb30e26556a51421f445.txt`

**Description:**
After the patient agreed to book a 12 PM appointment with “Dr. Dunty Hauser,” the office agent confirmed the appointment using multiple different provider names, including “Dr. Judy Hauser” and “Dr. Dugie Hauser.”

**Transcript Evidence:**
Agent: “I’d like to book the Thursday appointment with Dr. Dunty Hauser.”
User: “Just to confirm… with doctor Judy Hauser…”
User: “Your appointment is set… with doctor Dugie Hauser…”

**Why It’s a Problem:**
Incorrect provider confirmation can reduce patient trust and may result in scheduling errors if the wrong provider is recorded.

---

## Summary

These findings highlight key reliability challenges in voice AI systems:

* workflow state transition handling
* reconciliation of patient-reported vs system data
* consistency of critical entities (e.g., provider identity) during confirmation flows

Addressing these areas would improve conversational trust, reduce operational errors, and strengthen real-world deployment readiness.

# Outbound Healthcare Voice AI Agent

## Project Overview

This project implements an outbound healthcare voice AI agent designed to simulate realistic patient interactions such as appointment scheduling, rescheduling, cancellation, insurance verification, medication refill requests, and general inquiries.

The system makes real phone calls to another conversational agent, conducts multi-turn dialogues, captures call artifacts, and performs structured bug analysis to identify workflow reliability issues.

The primary goal of this project was to build a **working voice AI system and evaluate it through realistic conversational testing**, rather than focusing on infrastructure complexity.

---

## Key Capabilities

* Initiates real outbound phone calls using Retell AI
* Conducts multi-turn bot-to-bot healthcare conversations
* Handles structured workflows such as scheduling and cancellation
* Captures transcripts, recordings, and call metadata
* Exports audio artifacts in WAV and MP3 formats
* Uses scenario-driven testing to stress conversational workflows
* Performs AI-assisted bug discovery followed by manual validation

---

## System Architecture (High-Level)

```text
Scenario Object
   → Python Call Runner
   → Retell Voice Agent (Telephony + STT + LLM + TTS)
   → Healthcare Test Line / AI Receptionist
   → Transcript / Recording / Metadata Capture
   → Bug (AI 1st Pass) Analysis
```

For more details, see `docs/architecture.md`.

---

## Scenario-Driven Testing Approach

Each call is driven by a structured scenario object defining:

* patient persona
* conversation goal
* known facts
* behavioral style
* edge-case stress condition

This enables consistent testing across normal workflows and edge cases such as:

* ambiguous appointment intent
* mid-call workflow changes
* appointment record mismatches
* interruption handling
* backend workflow failures

The focus was on identifying **meaningful product risks**, not minor conversational imperfections.

---

## Bug Discovery Method

A hybrid analysis approach was used:

1. AI-assisted first pass on transcripts to identify potential workflow issues
2. manual review of transcript and audio recordings to confirm meaningful findings

Three key reliability issues were identified and documented in `bug_report.md`.


---

## Prerequisites

This project requires **ffmpeg** to be installed for audio conversion (WAV → MP3).

### Install ffmpeg

Download from:

https://ffmpeg.org/download.html

After installation, ensure the `ffmpeg` executable is available in your system PATH.

You can verify installation by running:

```bash
ffmpeg -version
```
If the command prints version information, the setup is complete.

---

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file:

```env
RETELL_API_KEY=your_api_key
RETELL_AGENT_ID=your_agent_id
RETELL_FROM_NUMBER=+1xxxx
RETELL_TO_NUMBER=+1xxxx
OPENAI_MODEL=gpt-4.1 (or other LLM mode)
OPENAI_API_KEY=xxxx (or other LLM api key)
```
The LLM is used only for offline transcript analysis — real phone calls are executed via Retell AI infrastructure.

### 3. Run a call

Default scenario:

```bash
python run_call.py
```

Run a specific scenario:

```bash
python run_call.py --scenario scenario_id
```

---

## Project Structure

```text
app/
   artifact_capture.py
   bug_analyzer.py
   call_runner.py
   config.py
   retell_api.py
   scenarios.py

docs/
   architecture.md
   bug_report.md

outputs/
   bug_analysis/
   logs/
   metadata/
   recordings/
   transcripts/

.env
requirements.txt
run_call.py
```

---

## Key Engineering Learnings

* Real-time voice AI systems are fundamentally stateful
* Conversational correctness alone does not guarantee workflow reliability
* Turn-taking latency and speech recognition variability affect user experience
* Scenario-driven testing can reveal meaningful risks

---

## System Artifacts

* Source code
* Real call transcripts
* Audio recordings
* Bug report
* Architecture documentation

---
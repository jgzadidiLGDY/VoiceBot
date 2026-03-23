# Architecture — Outbound Healthcare Voice AI Agent

## Overview

This project implements an outbound healthcare voice AI agent designed to simulate realistic conversational workflows such as appointment scheduling, cancellation, insurance verification, medication refill requests, and general inquiries.

The system performs real phone calls using Retell AI, conducts multi-turn conversations with another conversational agent, captures call artifacts, and analyzes conversations to identify reliability and workflow issues.

The primary architectural goal was to build a **working and testable voice AI system**, while intentionally avoiding unnecessary infrastructure complexity.

---

## System Design Principles

The architecture was guided by the following principles:

* Prioritize **working end-to-end functionality** over architectural elegance
* Use existing telephony and speech infrastructure rather than building custom stacks
* Focus on **scenario-driven testing** to uncover real conversational risks
* Keep orchestration lightweight and transparent
* Capture artifacts to enable **post-call analysis and iteration**

---

## High-Level Architecture Flow

```
Scenario Definition
        ↓
Python Call Orchestrator
        ↓
Retell Voice Agent (Telephony + STT + LLM + TTS)
        ↓
Healthcare Test Line / AI Receptionist
        ↓
Call Completion
        ↓
Artifact Capture (Transcript, Audio, Metadata)
        ↓
Bug (AI 1st pass) Analysis
```

---

## Core Components

### 1. Scenario Engine

Each outbound call is driven by a structured scenario object that defines:

* patient persona
* conversation goal
* known facts
* behavioral style
* edge-case stress condition

This enables consistent testing across workflows such as:

* new patient scheduling
* rescheduling and cancellation
* ambiguous intent
* insurance coverage verification
* medication refill requests
* interruption handling

Scenario-driven testing proved an effective way for early-stage validation.

---

### 2. Python Call Orchestrator

A lightweight Python runner is responsible for:

* loading environment configuration
* selecting a scenario
* injecting dynamic variables into the voice agent
* initiating outbound calls via Retell API
* polling call status until completion

This layer intentionally avoids complex state machines and instead relies on conversational testing to expose workflow limitations.

---

### 3. Voice Runtime Layer (Retell AI)

Retell provides the real-time voice infrastructure:

* outbound telephony connection
* speech-to-text transcription
* LLM-driven conversational reasoning
* text-to-speech playback

Using a managed voice platform enabled realistic latency behavior and conversational turn-taking characteristics without requiring custom telephony implementation.

---

### 4. Artifact Capture Pipeline

After each call completes, the system captures:

* full transcript
* audio recording (WAV + MP3 export)
* structured call metadata

Artifacts are stored locally in organized directories to support debugging, iteration, and demonstration of real system execution.

---

### 5. Bug Analysis Workflow

A hybrid bug discovery approach was implemented:

1. AI-assisted first pass to identify potential workflow issues
2. manual review of transcript and audio evidence

This process surfaced meaningful findings such as:

* inability of the workflow to pivot from rescheduling to cancellation during a live call
* insufficient clarification when patient-reported appointment details did not match system records
* inconsistent provider name confirmation during appointment booking 

The focus was on identifying **product-level risks**, not minor conversational imperfections.

---

## Architectural Tradeoffs

Several intentional tradeoffs were made:

* No custom telephony infrastructure was implemented
* Batch call execution was avoided to reflect real testing practices
* Conversational realism was prioritized over system abstraction layers

These decisions allowed faster iteration and more realistic validation of voice AI behavior.

---

## Key Learnings

The project highlighted that real-time voice AI systems are fundamentally **stateful and latency-sensitive**.

System reliability depends on:

* conversational state transitions
* entity verification mechanisms
* graceful handling of backend failures
* turn-taking calibration

Scenario-driven testing proved to be an effective strategy for uncovering meaningful risks in system development.

---

## Conclusion

This architecture demonstrates a practical approach to building and testing a voice AI agent in a healthcare-style environment.

By combining lightweight orchestration, realistic telephony execution, and structured scenario testing, the system provides:

* working conversational workflows
* reproducible call artifacts
* actionable reliability insights

This approach balances engineering discipline with product validation, which is essential for deploying voice AI systems in real-world settings.

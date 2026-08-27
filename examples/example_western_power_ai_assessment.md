# Public Sector AI Assurance Assessment

## AI Use Case

**Agency:** Western Power

**AI system:** AI model that predicts potential failures in electricity network assets

**Purpose:** Identify assets at higher risk of failure to support maintenance planning

## Assurance Assessment

This prototype identifies assurance areas that may require further review based on evidence retrieved from the government AI assurance framework.

### Privacy and security

**Status:** Review required

**Recommended action:** Review what information the AI system can access, whether personal or sensitive information may be processed, where prompts and responses are stored, and what security and access controls are required.

**Relevant policy evidence:**

- Page 3, Chunk 1 — matched concepts: privacy, security
- Page 10, Chunk 2 — matched concepts: data governance

### Reliability and testing

**Status:** Review required

**Recommended action:** Define a structured testing approach before deployment. Test the system against representative questions and edge cases, record incorrect or unsupported responses, establish acceptable performance criteria, and plan ongoing monitoring.

**Relevant policy evidence:**

- Page 24, Chunk 2 — matched concepts: testing, test, validation, reliable
- Page 3, Chunk 1 — matched concepts: test
- Page 10, Chunk 2 — matched concepts: testing, test, reliable
- Page 11, Chunk 2 — matched concepts: validation, monitor
- Page 24, Chunk 1 — matched concepts: testing, test, reliable
- Page 11, Chunk 3 — matched concepts: performance, monitor

### Human oversight

**Status:** Review required

**Recommended action:** Define where human review is required and make clear that users remain responsible for verifying important AI-generated outputs against authoritative source information.

**Relevant policy evidence:**

- Page 24, Chunk 2 — matched concepts: human oversight, human validation

### Accountability and governance

**Status:** Review required

**Recommended action:** Establish clear ownership for the AI system, including who approves its use, who manages risks, who responds to incidents, and how the system fits within existing governance and risk management processes.

**Relevant policy evidence:**

- Page 24, Chunk 2 — matched concepts: accountability
- Page 3, Chunk 1 — matched concepts: accountability
- Page 10, Chunk 2 — matched concepts: accountability, governance, risk management

### Transparency and explainability

**Status:** Review required

**Recommended action:** Document how the AI system works, what information it uses, its known limitations, the results of testing, and when users should independently verify an output.

**Relevant policy evidence:**

- Page 24, Chunk 2 — matched concepts: explainability, explanation, explain, records, document
- Page 3, Chunk 1 — matched concepts: transparency, explainability, explain
- Page 10, Chunk 2 — matched concepts: transparency, explain
- Page 24, Chunk 1 — matched concepts: transparency, explainability, explain, records

## Prototype Limitations

- Retrieval currently uses transparent keyword matching rather than semantic embeddings.
- Retrieved evidence may include sections that are only partially relevant to the use case.
- Recommended actions are currently generated using predefined rule-based guidance rather than a language model.
- The prototype identifies areas requiring consideration; it does not determine whether an AI system is safe, compliant or suitable for deployment.
- Findings should be reviewed by appropriately qualified technical, governance, legal, privacy and security specialists where relevant.

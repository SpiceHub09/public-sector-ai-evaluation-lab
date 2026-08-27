# Public Sector AI Evaluation Lab

A Python prototype for exploring how public-sector AI use cases can be assessed against government AI assurance guidance.

The project takes a proposed AI use case, identifies potentially relevant assurance areas, uses semantic retrieval to find supporting evidence from the **National Framework for the Assurance of Artificial Intelligence in Government**, and produces a structured assessment report with practical next actions and traceable source references.

The project was developed iteratively: V1 established a transparent keyword-based retrieval baseline, while V2 introduced sentence embeddings after testing showed that keyword matching could miss conceptually relevant policy evidence.

![Example AI assurance assessment](assets/western_power_assessment_preview.png)

## Why I Built This

AI teams working across government may encounter very different problems across agencies.

One engagement might involve evaluating an AI model, another may involve governance or documentation, while another may involve supporting the deployment or testing of an AI solution.

I built this prototype to explore a practical question:

> How could a technical team quickly perform an initial, transparent assessment of an unfamiliar public-sector AI use case while keeping the findings traceable to published government guidance?

Rather than attempting to automate an assurance decision, the prototype acts as an initial decision-support tool. It highlights areas that may require further investigation and preserves the evidence used in the assessment.

## What the Prototype Does

The user provides:

- agency or organisation
- AI system or solution
- purpose of the AI system
- data used by the system
- known concerns or risks

The prototype then:

1. loads the government AI assurance framework
2. cleans the extracted PDF text
3. splits the document into overlapping chunks while preserving page metadata
4. identifies assurance areas relevant to the supplied use case
5. retrieves potentially relevant sections of the framework
6. associates retrieved evidence with assurance areas
7. provides predefined practical next actions
8. generates a Markdown assessment report with source page references

## Current Assurance Areas

The prototype considers five assurance areas:

- Privacy and security
- Reliability and testing
- Human oversight
- Accountability and governance
- Transparency and explainability

The prototype distinguishes between:

- **Review required** — the use case triggered the assurance area and supporting policy evidence was retrieved.
- **Relevant - evidence not retrieved** — the use case triggered the assurance area, but the current retrieval method did not find supporting evidence.
- **Not triggered by supplied use case** — no indicators for the assurance area were identified from the information supplied.

These statuses are intended to support further investigation. They are not compliance or deployment decisions.

## Architecture

```text
Government AI Assurance Framework (PDF)
                |
                v
        Document extraction
                |
                v
           Text cleaning
                |
                v
     Page-aware text chunking
                |
                v
      Sentence embeddings
                |
                +-----------------------+
                                        |
User-supplied AI use case               |
        |                               |
        v                               |
Identify relevant assurance areas       |
        |                               |
        +-------------------------------+
                        |
                        v
              Semantic retrieval
                        |
                        v
            Evidence classification
                        |
                        v
             Structured assessment
                        |
                        v
             Markdown report output

## Project Structure

```text
public-sector-ai-evaluation-lab/
|
|-- data/
|   `-- government AI assurance framework
|
|-- outputs/
|   `-- generated assessment reports
|
|-- src/
|   |-- clean_text.py
|   |-- load_document.py
|   |-- chunk_document.py
|   |-- retrieve.py
|   |-- evaluate_use_case.py
|   |-- assess_use_case.py
|   |-- generate_report.py
|   `-- run_assessment.py
|
|-- tests/
|-- requirements.txt
`-- README.md
```

## Running the Prototype

Create and activate a Python virtual environment and install the required dependencies.

```bash
pip install -r requirements.txt
```

Run:

```bash
python src/run_assessment.py
```

The prototype will prompt for information about the AI use case.

Example:

```text
Agency or organisation:
Western Power

AI system or solution:
AI model that predicts potential failures in electricity network assets

Purpose of the AI system:
Identify assets at higher risk of failure to support maintenance planning

Data used by the AI system:
Historical asset condition, maintenance and failure data

Known concerns or risks:
reliability safety accuracy testing monitoring explainability accountability
```

A Markdown assessment is then generated in the `outputs` directory.

## Testing and Iteration

I deliberately started with simple, transparent logic so I could inspect how each stage of the pipeline behaved before introducing more complex AI components.

During development, I tested the prototype against contrasting scenarios.

### V1 to V2: Improving Retrieval

The first version of the prototype used transparent keyword matching to retrieve evidence from the assurance framework.

Testing identified an important limitation.

In a public-document summarisation scenario, `accuracy` was supplied as the primary concern. The prototype correctly identified **Reliability and testing** as a relevant assurance area, but V1 keyword retrieval returned no supporting policy evidence.

This happened because relevant sections of the framework discussed concepts such as **incorrect outputs, reliability, testing and validation** rather than necessarily using the exact word `accuracy`.

V2 introduced semantic retrieval using sentence embeddings.

I tested both retrieval approaches against the same query:

**Query:** `accuracy`

**V1 — keyword retrieval**

> No policy evidence retrieved.

**V2 — semantic retrieval**

The highest-ranked results included:

- guidance requiring incorrect AI outputs to be flagged and addressed
- guidance covering reliability, testing, technical validation and human validation

This demonstrated that semantic retrieval could identify conceptually relevant evidence even when the terminology used by the user differed from the terminology used in the framework.

The original keyword retriever remains in the repository as a baseline, and `compare_retrieval.py` can be used to compare the two approaches.

This iteration reflects a deliberate design approach: introduce additional technical complexity only where testing demonstrates that it addresses an observed limitation.


### Health AI agent

A fictional health-sector use case involved a generative AI agent answering staff questions from internal clinical and operational policy documents.

This scenario raised considerations including privacy, security, reliability, human oversight and accountability.

### Infrastructure predictive AI

A second scenario considered an AI model predicting potential electricity-network asset failures.

This tested whether the same assessment pipeline could be applied to a substantially different domain and AI capability without changing the underlying code.

### Public-document summarisation

A lower-risk scenario considered an AI tool summarising publicly available government reports, with accuracy supplied as the primary concern.

Testing this scenario exposed an important limitation in the initial design: assurance categories were being inferred primarily from retrieved policy text.

This meant an explicitly supplied concern such as `accuracy` could be missed if the initial keyword retrieval did not return a reliability-related policy section.

I therefore separated:

1. **identification of assurance areas from the characteristics of the use case**, and
2. **retrieval of policy evidence supporting those areas**.

This improved the transparency of the assessment and allowed the prototype to distinguish between an area that was not triggered and an area that was relevant but lacked retrieved evidence.

## Design Decisions

### Traceability

Page and chunk metadata are retained throughout the pipeline so assessment findings can be traced back to their source material.

### Transparent and modular logic

Assurance-area identification remains deliberately rule-based so the factors triggering each category are transparent and easy to inspect.

Policy retrieval evolved from V1 keyword matching to V2 semantic retrieval using sentence embeddings. The original keyword retriever remains available as a baseline for comparison.

### Human review

The prototype does not make automated approval, compliance or deployment decisions.

A failure to retrieve evidence is also not interpreted as evidence that no risk exists.

## Current Limitations

This is an exploratory prototype rather than a production assurance system.

Current limitations include:

- assurance categories are identified using predefined rule-based indicators
- semantic retrieval may still miss or imperfectly rank relevant policy material
- semantic similarity does not guarantee substantive relevance
- retrieved chunks may be only partially relevant
- recommendations are predefined rather than generated dynamically
- the current prototype uses one primary assurance framework
- no automated technical testing of an actual AI model or agent is performed
- no production deployment or authentication layer is included

Outputs should therefore be treated as prompts for further investigation rather than authoritative assurance findings.

## Future Development

Potential next iterations include:

- vector-based document search
- support for multiple government policies and technical standards
- LLM-assisted analysis grounded in retrieved evidence
- automated evaluation of AI-agent responses
- configurable assurance frameworks
- improved source citation
- automated test suites
- containerisation using Docker
- deployment into a cloud or controlled environment
- a lightweight web interface

## Technology

Current V2:

- Python
- pypdf
- sentence-transformers
- PyTorch
- sentence embeddings
- semantic similarity retrieval
- rule-based assurance classification
- Markdown report generation
- pytest

The architecture is intentionally modular.

V1's keyword retriever remains available as a baseline, while V2 uses a locally running sentence-transformer model to retrieve evidence based on semantic similarity.

The embedding model runs locally, so the current prototype does not require a paid LLM or embedding API.

## Status

**V2 — semantic retrieval prototype**

V1 established the end-to-end assessment pipeline using transparent keyword retrieval.

V2 introduces local sentence embeddings and semantic retrieval, improving the prototype's ability to find relevant government guidance when the wording of an AI use case differs from the terminology used in the source framework.

The project is intended as a learning and experimentation environment for public-sector AI evaluation, assurance and responsible implementation.
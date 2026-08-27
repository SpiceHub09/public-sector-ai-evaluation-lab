import json
import os

from dotenv import load_dotenv
from google import genai


# ---------------------------------------------------------
# LOAD THE GEMINI API KEY
# ---------------------------------------------------------
#
# My Gemini API key is stored locally in .env and excluded
# from Git.
#
# This keeps credentials separate from the source code so the
# project can remain safely available in a public repository.
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Check the local .env file."
    )


# Create the Gemini client.
client = genai.Client(
    api_key=api_key
)


def build_evidence_context(evidence):
    """
    Convert retrieved policy chunks into clearly labelled evidence.

    Each source retains its page and chunk number.

    I want the language model to know exactly where every piece of
    evidence came from so its findings can remain traceable to the
    government framework.
    """

    evidence_sections = []

    for result in evidence:

        evidence_sections.append(
            f"""
SOURCE_ID: page_{result['page_number']}_chunk_{result['chunk_number']}
PAGE: {result['page_number']}
CHUNK: {result['chunk_number']}

{result['text']}
""".strip()
        )

    return "\n\n---\n\n".join(
        evidence_sections
    )


def generate_llm_assessment(use_case, evidence):
    """
    Generate a structured, evidence-grounded assessment.

    Earlier in V3, I asked Gemini to produce a complete written
    assessment.

    That produced useful analysis, but it also gave the language
    model control over both the reasoning and the report format.

    In this version, Gemini performs the analysis but returns
    structured JSON.

    My Python application can then validate, process and format
    the result itself.
    """

    evidence_context = build_evidence_context(
        evidence
    )

    # ---------------------------------------------------------
    # BUILD THE GROUNDED PROMPT
    # ---------------------------------------------------------
    #
    # I explicitly restrict the model to the evidence supplied
    # by my semantic retrieval component.
    #
    # I also require every finding to reference a SOURCE_ID so
    # the application can validate the model's citations.
    prompt = f"""
You are assisting with an initial public-sector AI assurance review.

Analyse the AI use case using ONLY the government framework evidence
provided below.

IMPORTANT RULES:

- Do not invent legal, policy or technical requirements.
- Do not use outside knowledge as evidence.
- Do not say "must", "required" or "compliant" unless that level of
  obligation is clearly supported by the supplied evidence.
- Prefer wording such as "should consider", "the evidence indicates",
  or "further review is appropriate" where the source is advisory.
- Every finding must reference at least one SOURCE_ID supplied below.
- Only reference SOURCE_ID values that actually appear below.
- If the evidence is insufficient, say so.
- Return ONLY valid JSON.
- Do not wrap the JSON in Markdown code fences.

Return this structure:

{{
  "agency": "string",
  "ai_system": "string",
  "summary": "short overall assessment",
  "findings": [
    {{
      "assurance_area": "string",
      "finding": "string",
      "why_it_matters": "string",
      "recommended_action": "string",
      "source_ids": ["page_X_chunk_Y"]
    }}
  ],
  "further_review": ["string"]
}}


AI USE CASE

Agency:
{use_case['agency']}

AI system:
{use_case['ai_system']}

Purpose:
{use_case['purpose']}

Data:
{use_case['data']}

Known concerns:
{use_case['concerns']}


GOVERNMENT FRAMEWORK EVIDENCE

{evidence_context}
""".strip()

    # ---------------------------------------------------------
    # ASK GEMINI TO GENERATE THE ASSESSMENT
    # ---------------------------------------------------------

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    # Gemini returns text even though I've requested JSON.
    raw_response = interaction.output_text.strip()

    # Convert the returned JSON text into a Python dictionary.
    #
    # If the model returns malformed JSON, I want the application
    # to fail clearly rather than silently passing unpredictable
    # data further through the pipeline.
    try:
        structured_assessment = json.loads(
            raw_response
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Gemini did not return valid JSON."
        ) from error

    return structured_assessment


def validate_source_ids(structured_assessment, evidence):
    """
    Check that Gemini only cites policy chunks that were actually
    retrieved and supplied to it.

    A language model can generate convincing-looking citations that
    do not correspond to real evidence.

    I therefore validate the model's source references in Python
    rather than automatically trusting them.
    """

    # Build a set containing every legitimate SOURCE_ID supplied
    # to the language model.
    valid_source_ids = {
        f"page_{result['page_number']}_chunk_{result['chunk_number']}"
        for result in evidence
    }

    invalid_source_ids = []

    # Check every citation generated for every finding.
    for finding in structured_assessment.get(
        "findings",
        [],
    ):

        for source_id in finding.get(
            "source_ids",
            [],
        ):

            if source_id not in valid_source_ids:

                invalid_source_ids.append(
                    source_id
                )

    return invalid_source_ids


def attach_source_evidence(structured_assessment, evidence):
    """
    Attach the original retrieved policy text to each source cited
    by the language model.

    Source validation confirms that Gemini only references chunks
    that were actually supplied to it.

    However, a valid source ID alone does not prove that the source
    supports the model's interpretation.

    I therefore include the underlying policy evidence so a person
    can inspect the source material alongside each generated finding.
    """

    # Build a lookup table containing every retrieved source.
    evidence_lookup = {}

    for result in evidence:

        source_id = (
            f"page_{result['page_number']}_"
            f"chunk_{result['chunk_number']}"
        )

        evidence_lookup[source_id] = {
            "page_number": result["page_number"],
            "chunk_number": result["chunk_number"],
            "text": result["text"],
        }

    # Work through each finding generated by Gemini.
    for finding in structured_assessment.get(
        "findings",
        [],
    ):

        finding["source_evidence"] = []

        # Find and attach the original evidence for every source
        # cited by this finding.
        for source_id in finding.get(
            "source_ids",
            [],
        ):

            if source_id in evidence_lookup:

                source = evidence_lookup[
                    source_id
                ]

                finding["source_evidence"].append(
                    {
                        "source_id": source_id,
                        "page_number": source["page_number"],
                        "chunk_number": source["chunk_number"],
                        "text": source["text"],
                    }
                )

    return structured_assessment
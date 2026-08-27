# I need access to the source-code folder because the functions
# I'm testing live inside src rather than an installed Python package.
import sys
from pathlib import Path


# Find the root folder of this project.
project_root = Path(__file__).resolve().parents[1]

# Add the src folder to Python's import path so I can import
# the project functions into this test file.
sys.path.insert(
    0,
    str(project_root / "src"),
)


from assess_use_case import (
    identify_relevant_categories,
    classify_evidence,
    build_assessment,
)


def test_accuracy_triggers_reliability():
    """
    Check that an explicitly stated accuracy concern causes the
    prototype to identify Reliability and testing as relevant.

    I added this test because an earlier version of the prototype
    could miss an accuracy concern when the retrieval stage did not
    happen to return reliability-related evidence.
    """

    # Create a simple, relatively low-risk AI use case.
    test_use_case = {
        "agency": "Test agency",

        "ai_system":
            "AI tool that summarises publicly available reports",

        "purpose":
            "Help staff understand long public reports",

        "data":
            "Publicly available government documents",

        "concerns":
            "accuracy",
    }

    # Identify which assurance categories the prototype thinks
    # are relevant to this scenario.
    relevant_categories = identify_relevant_categories(
        test_use_case
    )

    # Accuracy should cause Reliability and testing to be triggered.
    assert "Reliability and testing" in relevant_categories

    # Privacy and security should not be triggered simply because
    # this is an AI system used by a government organisation.
    assert "Privacy and security" not in relevant_categories


def test_missing_evidence_is_not_treated_as_no_risk():
    """
    Check that a relevant assurance issue is not treated as safe
    simply because the retrieval stage failed to find policy evidence.

    Failure to retrieve evidence may indicate that retrieval needs
    improvement or manual review. It does not prove that the underlying
    assurance issue is irrelevant.
    """

    test_use_case = {
        "agency": "Test agency",

        "ai_system":
            "AI tool used to summarise public reports",

        "purpose":
            "Help staff understand long reports",

        "data":
            "Publicly available documents",

        "concerns":
            "accuracy",
    }

    # Identify the assurance areas triggered by the use case.
    relevant_categories = identify_relevant_categories(
        test_use_case
    )

    # Deliberately provide no retrieved policy evidence.
    #
    # This simulates a situation where the retrieval component
    # fails to find supporting material.
    empty_evidence = []

    categories = classify_evidence(
        empty_evidence,
        relevant_categories,
    )

    assessment = build_assessment(
        test_use_case,
        categories,
    )

    # Find the Reliability and testing result.
    reliability_result = next(
        area
        for area in assessment["assurance_areas"]
        if area["category"] == "Reliability and testing"
    )

    # Because accuracy triggered this category, the prototype
    # should preserve it as relevant even though retrieval found
    # no supporting evidence.
    assert (
        reliability_result["status"]
        == "Relevant - evidence not retrieved"
    )


def test_semantic_retrieval_finds_accuracy_evidence():
    """
    Check that V2 semantic retrieval can find relevant policy
    evidence for an accuracy concern.

    V1 keyword retrieval returned no evidence when the query was
    simply "accuracy".

    V2 should recognise that accuracy is conceptually related to
    framework guidance about incorrect outputs, reliability,
    testing and validation.
    """

    from semantic_retrieve import semantic_retrieve

    # Use the same query that exposed the limitation in V1.
    results = semantic_retrieve(
        query="accuracy",
        top_k=5,
    )

    # The semantic retriever should return policy evidence.
    assert len(results) > 0

    # Combine the retrieved text so I can inspect whether the
    # results contain reliability/testing concepts.
    retrieved_text = " ".join(
        result["text"].lower()
        for result in results
    )

    expected_concepts = [
        "incorrect",
        "reliability",
        "reliable",
        "testing",
        "validation",
    ]

    # At least one expected concept should appear in the retrieved
    # evidence.
    assert any(
        concept in retrieved_text
        for concept in expected_concepts
    )


def test_valid_llm_source_ids_pass_validation():
    """
    Check that V3 source validation accepts citations corresponding
    to policy evidence that was genuinely retrieved and supplied
    to the language model.

    I want source validation to happen in Python rather than
    automatically trusting references generated by the LLM.
    """

    from llm_assessment import validate_source_ids

    # Create a small piece of simulated retrieved evidence.
    evidence = [
        {
            "page_number": 24,
            "chunk_number": 2,
            "text":
                "Example policy evidence about testing.",
        }
    ]

    # Simulate a structured LLM finding that correctly references
    # the evidence supplied to it.
    structured_assessment = {
        "findings": [
            {
                "assurance_area":
                    "Reliability and testing",

                "source_ids": [
                    "page_24_chunk_2"
                ],
            }
        ]
    }

    invalid_sources = validate_source_ids(
        structured_assessment,
        evidence,
    )

    # A legitimate source reference should produce no errors.
    assert invalid_sources == []


def test_invalid_llm_source_id_is_detected():
    """
    Check that V3 detects a source reference invented by the
    language model.

    A convincing-looking citation should not be accepted unless
    that source was genuinely retrieved and supplied to the model.
    """

    from llm_assessment import validate_source_ids

    evidence = [
        {
            "page_number": 24,
            "chunk_number": 2,
            "text":
                "Example policy evidence about testing.",
        }
    ]

    # Simulate the LLM inventing a citation that was never
    # retrieved.
    structured_assessment = {
        "findings": [
            {
                "assurance_area":
                    "Reliability and testing",

                "source_ids": [
                    "page_99_chunk_7"
                ],
            }
        ]
    }

    invalid_sources = validate_source_ids(
        structured_assessment,
        evidence,
    )

    # Python should detect the invented citation.
    assert invalid_sources == [
        "page_99_chunk_7"
    ]
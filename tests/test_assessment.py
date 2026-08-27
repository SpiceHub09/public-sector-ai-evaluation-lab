# I need access to the source-code folder because the functions
# I'm testing currently live inside src rather than an installed
# Python package.
import sys
from pathlib import Path


# Find the root folder of this project.
project_root = Path(__file__).resolve().parents[1]

# Add the src folder to Python's import path so I can import
# the assessment functions into this test file.
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
    prototype to identify reliability and testing as relevant.

    I added this test because an earlier version of the prototype
    could miss an accuracy concern when the initial policy retrieval
    did not happen to return reliability-related evidence.

    This test protects the behaviour I introduced when I separated
    use-case risk identification from policy-evidence retrieval.
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

    This is an important design principle in the prototype.

    Failure to retrieve evidence means the retrieval process may need
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

    I added this test because V1 keyword retrieval returned no
    evidence when the query was simply "accuracy".

    V2 should recognise that accuracy is conceptually related to
    framework guidance about incorrect outputs, reliability,
    testing and validation, even when the exact word "accuracy"
    is not present.
    """

    # Import the V2 semantic retrieval function here so this test
    # specifically evaluates the new retrieval approach.
    from semantic_retrieve import semantic_retrieve

    # Use the same query that exposed the limitation in V1.
    results = semantic_retrieve(
        query="accuracy",
        top_k=5,
    )

    # The semantic retriever should return policy evidence.
    assert len(results) > 0

    # Combine the retrieved text so I can check whether the
    # results contain concepts relevant to reliability and testing.
    retrieved_text = " ".join(
        result["text"].lower()
        for result in results
    )

    # I expect the retrieved evidence to contain at least one
    # concept associated with reliability or testing.
    expected_concepts = [
        "incorrect",
        "reliability",
        "reliable",
        "testing",
        "validation",
    ]

    assert any(
        concept in retrieved_text
        for concept in expected_concepts
    )
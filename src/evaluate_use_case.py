from retrieve import retrieve_relevant_chunks
from chunk_document import chunks


def build_search_query(use_case):
    """
    Turn an agency AI use case into a focused search query.

    In my first version, I combined almost every part of the use case
    into the search query.

    After testing the retrieval results, I found that this introduced
    too many broad words such as "government", "policy" and "internal".
    These words appeared frequently throughout the document and could
    make irrelevant sections look more important than they really were.

    For this version, I want the search to focus more heavily on the
    actual AI capability and the assurance concerns I need to investigate.
    """

    # Use the type of AI system together with the specific risks and
    # assurance issues I want to investigate.
    #
    # I'm deliberately leaving out the broader agency description,
    # purpose and data fields for now because they contain many generic
    # words that do not help distinguish relevant policy sections.
    query = (
        f"{use_case['ai_system']} "
        f"{use_case['concerns']}"
    )

    return query


def gather_policy_evidence(use_case, policy_chunks, top_k=6):
    """
    Retrieve the parts of the government AI assurance framework
    that are most relevant to a proposed agency AI use case.

    I want the assessment to be grounded in published government
    guidance rather than relying only on a language model's
    general knowledge.
    """

    # First, turn the agency use case into a focused search query.
    query = build_search_query(use_case)

    # Search the policy chunks and keep only the strongest matches.
    #
    # I'm retrieving six sections for now because I want enough
    # evidence to cover different assurance issues without using
    # the entire framework.
    evidence = retrieve_relevant_chunks(
        query=query,
        chunks=policy_chunks,
        top_k=top_k,
    )

    return evidence


# ---------------------------------------------------------
# SAMPLE AGENCY USE CASE
# ---------------------------------------------------------
#
# I'm starting with a fictional health-sector scenario.
#
# This reflects the type of assignment a public-sector AI team
# could receive: an agency already has an idea for an AI solution
# and needs technical and assurance support before using it.
#
# Keeping the scenario as structured data also means I can later
# replace it with other agency use cases without changing the
# underlying retrieval and assessment logic.


use_case = {
    "agency": "WA health agency",

    "ai_system":
        "Generative AI agent that answers staff questions using "
        "internal clinical and operational policy documents",

    "purpose":
        "Help employees find relevant internal policy information "
        "more quickly",

    "data":
        "Internal government policy documents and staff questions",

    "concerns":
        "accuracy hallucination privacy security human oversight "
        "testing monitoring governance accountability",
}


# Retrieve government guidance relevant to this proposed AI system.
#
# Other parts of the application can import this evidence and use it
# without needing to repeat the retrieval process themselves.
evidence = gather_policy_evidence(
    use_case=use_case,
    policy_chunks=chunks,
)


# ---------------------------------------------------------
# TEST THE USE-CASE EVALUATION
# ---------------------------------------------------------
#
# I only want this detailed preview to appear when I execute
# evaluate_use_case.py directly.
#
# assess_use_case.py imports use_case and evidence from this file.
# Without this check, the entire retrieval preview would print every
# time another part of the application imported those variables.
#
# Using __name__ == "__main__" lets me keep the manual test available
# while separating it from the reusable application logic.


if __name__ == "__main__":

    # Display the agency scenario I'm evaluating.
    print("\n" + "=" * 70)
    print("AI USE CASE")
    print("=" * 70)

    print(f"\nAgency: {use_case['agency']}")
    print(f"AI system: {use_case['ai_system']}")
    print(f"Purpose: {use_case['purpose']}")
    print(f"Data: {use_case['data']}")

    # Display the policy evidence retrieved for this scenario.
    #
    # I want to be able to inspect these results manually because
    # retrieval quality directly affects the quality of any
    # assessment built from this evidence.
    print("\n" + "=" * 70)
    print("RETRIEVED POLICY EVIDENCE")
    print("=" * 70)

    for result in evidence:

        print("\n" + "-" * 70)

        print(
            f"Page: {result['page_number']} | "
            f"Chunk: {result['chunk_number']} | "
            f"Retrieval score: {result['score']}"
        )

        print("\n" + result["text"])
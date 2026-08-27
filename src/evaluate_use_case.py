from semantic_retrieve import semantic_retrieve


def build_search_query(use_case):
    """
    Turn an agency AI use case into a focused semantic search query.

    V1 of my prototype used keyword matching to retrieve relevant
    sections of the government AI assurance framework.

    Testing showed that this could miss relevant guidance when the
    use case and the framework expressed the same idea using different
    words.

    For example, the concern "accuracy" did not retrieve framework
    guidance about incorrect outputs, reliability, testing or validation.

    V2 therefore uses semantic retrieval so the search can consider
    similarity of meaning rather than relying only on exact words.
    """

    # Combine the description of the AI system with the concerns
    # identified for the use case.
    #
    # These provide the semantic retriever with information about
    # both what the system does and what assurance issues need
    # investigation.
    query = (
        f"{use_case['ai_system']} "
        f"{use_case['concerns']}"
    )

    return query


def gather_policy_evidence(use_case, policy_chunks=None, top_k=6):
    """
    Retrieve government guidance that is semantically relevant
    to the proposed AI use case.

    The policy_chunks argument is retained for compatibility with
    the existing application structure, but V2 semantic retrieval
    already works with the policy chunks prepared in
    semantic_retrieve.py.

    I retrieve a small number of strong matches rather than passing
    the entire framework into the assessment process.
    """

    # Turn the agency scenario into a semantic search query.
    query = build_search_query(
        use_case
    )

    # Search the government framework using embeddings.
    #
    # Unlike V1 keyword retrieval, this can find relevant guidance
    # even where the wording differs from the terminology supplied
    # by the user.
    evidence = semantic_retrieve(
        query=query,
        top_k=top_k,
    )

    return evidence


# ---------------------------------------------------------
# SAMPLE AGENCY USE CASE
# ---------------------------------------------------------
#
# I keep a fictional health-sector scenario available for
# testing individual components of the application.
#
# run_assessment.py can supply completely different scenarios
# without changing the underlying assessment code.


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


# Retrieve semantically relevant government guidance for the
# sample health-sector scenario.
evidence = gather_policy_evidence(
    use_case=use_case,
)


# ---------------------------------------------------------
# TEST V2 RETRIEVAL
# ---------------------------------------------------------
#
# I only want this detailed preview when I execute this file
# directly.
#
# Other parts of the application can import use_case and evidence
# without printing the retrieval results.


if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("AI USE CASE - SEMANTIC RETRIEVAL")
    print("=" * 70)

    print(f"\nAgency: {use_case['agency']}")
    print(f"AI system: {use_case['ai_system']}")
    print(f"Purpose: {use_case['purpose']}")
    print(f"Data: {use_case['data']}")

    print("\n" + "=" * 70)
    print("SEMANTICALLY RETRIEVED POLICY EVIDENCE")
    print("=" * 70)

    for result in evidence:

        print("\n" + "-" * 70)

        print(
            f"Similarity: {result['score']:.3f} | "
            f"Page: {result['page_number']} | "
            f"Chunk: {result['chunk_number']}"
        )

        print("\n" + result["text"])
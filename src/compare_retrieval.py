from retrieve import retrieve_relevant_chunks
from chunk_document import chunks
from semantic_retrieve import semantic_retrieve


def compare_retrieval_methods(query, top_k=5):
    """
    Compare the original keyword retrieval approach with the newer
    semantic retrieval approach.

    I want to keep V1 available as a baseline rather than simply
    replacing it.

    This lets me test whether introducing embeddings actually improves
    retrieval for problems that the keyword approach struggled with.
    """

    # ---------------------------------------------------------
    # V1: KEYWORD RETRIEVAL
    # ---------------------------------------------------------
    #
    # My original retriever looks for meaningful words that appear
    # in both the query and the policy chunk.
    keyword_results = retrieve_relevant_chunks(
        query=query,
        chunks=chunks,
        top_k=top_k,
    )

    # ---------------------------------------------------------
    # V2: SEMANTIC RETRIEVAL
    # ---------------------------------------------------------
    #
    # The semantic retriever compares embeddings instead of relying
    # on exact terminology.
    #
    # This should help when the user's wording and the framework's
    # wording express similar ideas using different words.
    semantic_results = semantic_retrieve(
        query=query,
        top_k=top_k,
    )

    return keyword_results, semantic_results


if __name__ == "__main__":

    # I'm deliberately using "accuracy" because this exposed a
    # limitation during V1 testing.
    #
    # The framework contains relevant guidance about incorrect
    # outputs, reliability, testing and validation, but those sections
    # do not necessarily use the exact word "accuracy".
    query = "accuracy"

    keyword_results, semantic_results = compare_retrieval_methods(
        query=query,
        top_k=5,
    )

    print("\n" + "=" * 70)
    print("RETRIEVAL COMPARISON")
    print("=" * 70)

    print(f"\nQuery: {query}")

    # ---------------------------------------------------------
    # SHOW V1 RESULTS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("V1 - KEYWORD RETRIEVAL")
    print("=" * 70)

    if keyword_results:

        for result in keyword_results:

            print("\n" + "-" * 70)

            print(
                f"Score: {result['score']} | "
                f"Page: {result['page_number']} | "
                f"Chunk: {result['chunk_number']}"
            )

            # Show only a short preview so the comparison remains
            # readable in the terminal.
            print(
                "\n"
                + result["text"][:300]
                + "..."
            )

    else:

        print(
            "\nNo policy evidence retrieved using keyword matching."
        )

    # ---------------------------------------------------------
    # SHOW V2 RESULTS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("V2 - SEMANTIC RETRIEVAL")
    print("=" * 70)

    for result in semantic_results:

        print("\n" + "-" * 70)

        print(
            f"Similarity: {result['score']:.3f} | "
            f"Page: {result['page_number']} | "
            f"Chunk: {result['chunk_number']}"
        )

        print(
            "\n"
            + result["text"][:300]
            + "..."
        )
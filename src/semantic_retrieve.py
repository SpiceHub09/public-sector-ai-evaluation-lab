from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from chunk_document import chunks


# ---------------------------------------------------------
# LOAD THE EMBEDDING MODEL
# ---------------------------------------------------------
#
# I'm using the same small embedding model I tested earlier.
#
# Instead of matching exact words, this model represents the
# meaning of each piece of text numerically.
#
# This should allow the retrieval process to find relevant policy
# guidance even when the user's wording differs from the wording
# used in the government framework.
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# CREATE EMBEDDINGS FOR THE POLICY
# ---------------------------------------------------------
#
# Each item in chunks contains a small section of the government
# framework together with its original page and chunk number.
#
# I only need the text itself when creating embeddings.
chunk_texts = [
    chunk["text"]
    for chunk in chunks
]


# Convert all of the policy chunks into embeddings.
#
# I do this once here so I can compare future queries against
# the same numerical representations of the policy.
chunk_embeddings = model.encode(
    chunk_texts,
    convert_to_tensor=True,
)


def semantic_retrieve(query, top_k=5):
    """
    Retrieve policy chunks based on similarity of meaning rather
    than exact keyword matches.

    V1 of my prototype used keyword retrieval.

    Testing showed that keyword retrieval could miss relevant
    guidance when the use case and the policy expressed the same
    idea using different words.

    This V2 retrieval approach uses embeddings to compare semantic
    similarity instead.
    """

    # Convert the user's query into an embedding using the same
    # model I used for the policy chunks.
    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
    )

    # Compare the meaning of the query with the meaning of every
    # policy chunk.
    similarities = cos_sim(
        query_embedding,
        chunk_embeddings,
    )[0]

    # I'll store each policy chunk together with its semantic
    # similarity score.
    scored_chunks = []

    for index, similarity in enumerate(similarities):

        chunk = chunks[index]

        scored_chunks.append(
            {
                "score": float(similarity),
                "page_number": chunk["page_number"],
                "chunk_number": chunk["chunk_number"],
                "text": chunk["text"],
            }
        )

    # Sort the results so the policy chunks with meanings most
    # similar to the query appear first.
    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # Return only the strongest matches.
    return scored_chunks[:top_k]


# ---------------------------------------------------------
# TEST SEMANTIC RETRIEVAL
# ---------------------------------------------------------
#
# I want to test V2 against a problem I observed in V1.
#
# In my public-document summarisation scenario, the user explicitly
# identified "accuracy" as a concern.
#
# V1 correctly recognised that this related to reliability and
# testing, but its keyword retrieval did not find supporting
# policy evidence.
#
# I want to see whether semantic retrieval can find relevant
# guidance based on meaning instead.


if __name__ == "__main__":

    query = "accuracy"

    results = semantic_retrieve(
        query=query,
        top_k=5,
    )

    print("\n" + "=" * 70)
    print("SEMANTIC RETRIEVAL TEST")
    print("=" * 70)

    print(f"\nQuery: {query}")

    for result in results:

        print("\n" + "-" * 70)

        print(
            f"Similarity: {result['score']:.3f} | "
            f"Page: {result['page_number']} | "
            f"Chunk: {result['chunk_number']}"
        )

        print("\n" + result["text"])
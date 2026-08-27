import re

from chunk_document import chunks


def score_chunk(query, chunk_text):
    """
    Give a relevance score to a policy chunk based on meaningful
    words shared between the query and the chunk.

    My first version simply split the query wherever there was a space.
    That was useful for proving that retrieval worked, but it also gave
    too much weight to common words.

    Here, I'm making the keyword retrieval slightly more selective
    while still keeping it simple and transparent.
    """

    # These common words do not tell me much about whether a policy
    # section is genuinely relevant to an AI assurance question.
    #
    # Removing them helps the retrieval focus on more informative
    # concepts such as privacy, testing, oversight and accountability.
    stop_words = {
        "the",
        "and",
        "that",
        "this",
        "with",
        "using",
        "use",
        "for",
        "from",
        "into",
        "their",
        "internal",
        "government",
        "policy",
        "documents",
        "staff",
        "questions",
        "system",
        "systems",
    }

    # Extract words using a regular expression rather than relying
    # only on spaces.
    #
    # This also removes punctuation and makes all terms lowercase.
    query_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", query.lower())
    )

    chunk_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", chunk_text.lower())
    )

    # Remove common words from the query.
    query_words = query_words - stop_words

    # Count how many meaningful query concepts also appear
    # in the current policy chunk.
    matching_words = query_words.intersection(chunk_words)

    score = len(matching_words)

    return score


def retrieve_relevant_chunks(query, chunks, top_k=5):
    """
    Search all policy chunks and return the most relevant ones.

    I want the application to retrieve a small number of useful
    sections from the policy instead of passing the entire document
    to an AI model.
    """

    # I'll store each chunk together with its relevance score.
    scored_chunks = []

    # Work through every chunk created from the policy.
    for chunk in chunks:

        # Calculate how relevant the current chunk is to the query.
        score = score_chunk(query, chunk["text"])

        # I only want to keep chunks that matched at least
        # part of the query.
        if score > 0:
            scored_chunks.append(
                {
                    "score": score,
                    "page_number": chunk["page_number"],
                    "chunk_number": chunk["chunk_number"],
                    "text": chunk["text"],
                }
            )

    # Sort the chunks from highest relevance score to lowest.
    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # Return only the most relevant results.
    return scored_chunks[:top_k]


# ---------------------------------------------------------
# TEST THE RETRIEVAL PROCESS
# ---------------------------------------------------------
#
# I only want this test to run when I execute retrieve.py directly.
#
# Other parts of the project import retrieve_relevant_chunks from
# this file. I don't want this sample query and its results to print
# every time another part of the application uses the retrieval
# function.
#
# Using __name__ == "__main__" lets me keep this useful test here
# while separating it from the reusable retrieval logic.


if __name__ == "__main__":

    # Test the retrieval process with a sample assurance question.
    #
    # I'm using a governance-related query because I expect the
    # assurance framework to contain relevant material on this topic.
    query = "human oversight risk governance"

    results = retrieve_relevant_chunks(
        query=query,
        chunks=chunks,
        top_k=5,
    )

    # Check how many relevant chunks were returned.
    print(f"\nQuery: {query}")
    print(f"Relevant chunks found: {len(results)}")

    # Show each retrieved chunk so I can manually inspect whether
    # the retrieval results actually make sense.
    for result in results:

        print("\n" + "-" * 60)

        print(
            f"Score: {result['score']} | "
            f"Page: {result['page_number']} | "
            f"Chunk: {result['chunk_number']}"
        )

        print("\n" + result["text"])
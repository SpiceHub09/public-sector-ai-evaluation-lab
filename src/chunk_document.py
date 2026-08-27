from load_document import pages_text


def chunk_pages(pages, chunk_size=800, overlap=150):
    """
    Break the cleaned PDF pages into smaller overlapping chunks.

    I want to work with smaller sections of the framework rather than
    searching or analysing an entire page at once.

    Keeping some overlap between chunks also helps preserve context
    where an important sentence or idea sits close to a chunk boundary.
    """

    # I'll store all of the chunks I create in this list.
    chunks = []

    # Work through one cleaned PDF page at a time.
    for page in pages:

        # Keep the original page number so I can later trace
        # retrieved evidence back to the source document.
        page_number = page["page_number"]

        # This is the cleaned text I extracted from the current page.
        text = page["text"]

        # Some PDF pages may contain no useful extracted text.
        #
        # If that happens, I'll skip the page rather than creating
        # an empty chunk.
        if not text:
            continue

        # start tells me where the current chunk begins
        # within the page text.
        start = 0

        # I'll number the chunks within each page.
        #
        # This gives me another simple identifier that I can use
        # when inspecting retrieval and assessment results.
        chunk_number = 1

        # Continue creating chunks until I've worked through
        # all of the text on the current page.
        while start < len(text):

            # Each chunk will contain up to 800 characters.
            end = start + chunk_size

            # Extract the current section of text.
            #
            # strip() removes unnecessary whitespace from the
            # beginning and end of the chunk.
            chunk_text = text[start:end].strip()

            # Store the chunk together with information about
            # where it came from.
            #
            # I want to retain this metadata because later,
            # if the application retrieves this chunk as evidence,
            # I can show the original page and chunk number.
            chunks.append(
                {
                    "page_number": page_number,
                    "chunk_number": chunk_number,
                    "text": chunk_text,
                }
            )

            # Move to the next chunk number for this page.
            chunk_number += 1

            # Move forward through the page text.
            #
            # I'm deliberately moving forward by less than the full
            # chunk size so that 150 characters overlap with the
            # previous chunk.
            #
            # For example:
            #
            # Chunk 1: characters 0-800
            # Chunk 2: characters 650-1450
            #
            # This reduces the chance of losing important context
            # where information sits across two chunks.
            start += chunk_size - overlap

    # Return all of the chunks created from the framework.
    return chunks


# Create chunks from the cleaned policy pages I loaded earlier.
#
# Other parts of the project can now import this collection and
# search it without needing to repeat the chunking logic.
chunks = chunk_pages(pages_text)


# ---------------------------------------------------------
# TEST THE CHUNKING PROCESS
# ---------------------------------------------------------
#
# I only want this preview to appear when I run this file directly.
#
# Other parts of the application need to import the chunks, but they
# don't need to repeatedly print my chunking test output.
#
# Keeping the test inside this block separates the reusable chunking
# logic from the code I'm using to manually inspect its behaviour.


if __name__ == "__main__":

    # Check how many chunks were created from the full document.
    print(f"\nTotal chunks created: {len(chunks)}")

    # Preview the first chunk so I can confirm that:
    #
    # 1. the original page number has been preserved,
    # 2. the chunk numbering is working, and
    # 3. the text still looks sensible after being split.
    print("\n--- FIRST CHUNK ---\n")

    print(f"Page: {chunks[0]['page_number']}")
    print(f"Chunk: {chunks[0]['chunk_number']}")
    print(chunks[0]["text"])
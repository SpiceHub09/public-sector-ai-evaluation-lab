import re


def clean_page_text(text):
    """
    Clean text extracted from a PDF so it is easier to search,
    analyse and eventually pass to an AI model.
    """

    # PDF extraction often leaves multiple spaces or tabs between words.
    # I want to reduce these to a single space so the text is more consistent.
    text = re.sub(r"[ \t]+", " ", text)

    # PDFs can also introduce several blank lines between sections.
    # I'll keep paragraph breaks, but remove excessive empty lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces that appear immediately before a new line.
    # This helps tidy up formatting artefacts created during PDF extraction.
    text = re.sub(r" +\n", "\n", text)

    # Remove unnecessary spaces from the very beginning and end
    # of each page's extracted text.
    text = text.strip()

    return text
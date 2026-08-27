from pathlib import Path


def generate_rag_markdown_report(structured_assessment):
    """
    Turn the structured RAG assessment into a readable Markdown report.

    Gemini performs the evidence-grounded analysis, but I want my
    application to control how the final report is presented.

    This separation means the language model is responsible for
    reasoning while Python remains responsible for structure,
    traceability and presentation.
    """

    report_lines = []

    # ---------------------------------------------------------
    # REPORT TITLE
    # ---------------------------------------------------------

    report_lines.append(
        "# Public Sector AI Assurance Assessment"
    )

    report_lines.append("")

    report_lines.append(
        "**Assessment method:** "
        "Semantic retrieval + evidence-grounded LLM analysis"
    )

    report_lines.append("")

    # ---------------------------------------------------------
    # USE-CASE SUMMARY
    # ---------------------------------------------------------

    report_lines.append(
        "## AI Use Case"
    )

    report_lines.append("")

    report_lines.append(
        f"**Agency:** "
        f"{structured_assessment['agency']}"
    )

    report_lines.append("")

    report_lines.append(
        f"**AI system:** "
        f"{structured_assessment['ai_system']}"
    )

    report_lines.append("")

    # ---------------------------------------------------------
    # OVERALL SUMMARY
    # ---------------------------------------------------------

    report_lines.append(
        "## Initial Assessment"
    )

    report_lines.append("")

    report_lines.append(
        structured_assessment["summary"]
    )

    report_lines.append("")

    # ---------------------------------------------------------
    # FINDINGS
    # ---------------------------------------------------------

    report_lines.append(
        "## Assurance Findings"
    )

    report_lines.append("")

    for number, finding in enumerate(
        structured_assessment["findings"],
        start=1,
    ):

        report_lines.append(
            f"### {number}. "
            f"{finding['assurance_area']}"
        )

        report_lines.append("")

        report_lines.append(
            f"**Finding:** "
            f"{finding['finding']}"
        )

        report_lines.append("")

        report_lines.append(
            f"**Why it matters:** "
            f"{finding['why_it_matters']}"
        )

        report_lines.append("")

        report_lines.append(
            f"**Recommended action:** "
            f"{finding['recommended_action']}"
        )

        report_lines.append("")

        # -----------------------------------------------------
        # TRACEABLE EVIDENCE
        # -----------------------------------------------------
        #
        # I include the actual policy text that was retrieved and
        # supplied to the language model.
        #
        # This allows a reviewer to inspect whether the source
        # evidence genuinely supports the generated finding.

        report_lines.append(
            "**Supporting framework evidence:**"
        )

        report_lines.append("")

        for source in finding.get(
            "source_evidence",
            [],
        ):

            report_lines.append(
                f"**Page {source['page_number']}, "
                f"Chunk {source['chunk_number']}**"
            )

            report_lines.append("")

            # Convert line breaks inside the extracted PDF text
            # into spaces so the Markdown evidence block is easier
            # to read.
            evidence_text = (
                source["text"]
                .replace("\n", " ")
            )

            report_lines.append(
                f"> {evidence_text}"
            )

            report_lines.append("")

    # ---------------------------------------------------------
    # FURTHER REVIEW
    # ---------------------------------------------------------

    report_lines.append(
        "## Further Review"
    )

    report_lines.append("")

    for item in structured_assessment.get(
        "further_review",
        [],
    ):

        report_lines.append(
            f"- {item}"
        )

    report_lines.append("")

    # ---------------------------------------------------------
    # IMPORTANT LIMITATION
    # ---------------------------------------------------------

    report_lines.append(
        "## Important Note"
    )

    report_lines.append("")

    report_lines.append(
        "This is an exploratory AI-assisted assessment. "
        "Semantic retrieval and language-model analysis can miss, "
        "misinterpret or overstate relevant guidance. The included "
        "source evidence is provided to support human verification "
        "of generated findings. The output should not be treated as "
        "a compliance, legal or deployment decision."
    )

    report_lines.append("")

    return "\n".join(
        report_lines
    )


def save_rag_report(
    report_text,
    structured_assessment,
):
    """
    Save the RAG-generated assessment separately from the original
    rule-based assessment reports.

    I want the filename to make clear that this report was produced
    using the RAG pipeline.
    """

    output_directory = Path(
        "outputs"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Convert the agency name into a simple filename.
    agency_name = (
        structured_assessment["agency"]
        .lower()
        .strip()
        .replace(" ", "_")
    )

    filename = (
        f"{agency_name}_rag_assessment.md"
    )

    output_path = (
        output_directory
        / filename
    )

    output_path.write_text(
        report_text,
        encoding="utf-8",
    )

    return output_path
from pathlib import Path

from assess_use_case import assessment


def generate_markdown_report(assessment):
    """
    Turn the structured AI assurance assessment into a readable
    Markdown report.

    I want the report to clearly distinguish between:

    - assurance areas that were triggered and have supporting evidence,
    - assurance areas that were triggered but where evidence was not
      retrieved, and
    - assurance areas that were not triggered by the supplied use case.

    This makes the report easier to interpret and avoids presenting
    recommendations for areas that the prototype did not identify as
    relevant.
    """

    # I'll build the report one section at a time and store each
    # section in this list.
    report_lines = []

    # ---------------------------------------------------------
    # REPORT TITLE
    # ---------------------------------------------------------

    report_lines.append("# Public Sector AI Assurance Assessment")
    report_lines.append("")

    # ---------------------------------------------------------
    # USE-CASE SUMMARY
    # ---------------------------------------------------------

    report_lines.append("## AI Use Case")
    report_lines.append("")

    report_lines.append(
        f"**Agency:** {assessment['agency']}"
    )

    report_lines.append("")

    report_lines.append(
        f"**AI system:** {assessment['ai_system']}"
    )

    report_lines.append("")

    report_lines.append(
        f"**Purpose:** {assessment['purpose']}"
    )

    report_lines.append("")

    # ---------------------------------------------------------
    # ASSURANCE ASSESSMENT
    # ---------------------------------------------------------

    report_lines.append("## Assurance Assessment")
    report_lines.append("")

    report_lines.append(
        "This prototype identifies assurance areas that may require "
        "further review based on the characteristics of the supplied "
        "AI use case and evidence retrieved from the government AI "
        "assurance framework."
    )

    report_lines.append("")

    # Work through each assurance area identified by the
    # assessment process.
    for area in assessment["assurance_areas"]:

        report_lines.append(
            f"### {area['category']}"
        )

        report_lines.append("")

        # Show the assessment status for this assurance area.
        report_lines.append(
            f"**Status:** {area['status']}"
        )

        report_lines.append("")

        # Show which characteristics of the supplied use case
        # caused this assurance area to be triggered.
        if area.get("matched_indicators"):

            matched_indicators = ", ".join(
                area["matched_indicators"]
            )

            report_lines.append(
                f"**Use-case indicators:** {matched_indicators}"
            )

            report_lines.append("")

        # Only provide a recommended action when the assurance
        # area was actually triggered by the supplied use case.
        #
        # If the category was not triggered, displaying a
        # recommendation could make the report appear to
        # contradict its own assessment.
        if area["status"] != "Not triggered by supplied use case":

            report_lines.append(
                f"**Recommended action:** {area['recommendation']}"
            )

            report_lines.append("")

        # ---------------------------------------------------------
        # POLICY EVIDENCE
        # ---------------------------------------------------------

        if area["evidence"]:

            report_lines.append(
                "**Relevant policy evidence:**"
            )

            report_lines.append("")

            for item in area["evidence"]:

                matched_keywords = ", ".join(
                    item["matched_keywords"]
                )

                report_lines.append(
                    f"- Page {item['page_number']}, "
                    f"Chunk {item['chunk_number']} "
                    f"— matched concepts: {matched_keywords}"
                )

        else:

            # If the assurance area was not triggered, I want the
            # report to make clear that the prototype did not identify
            # indicators for that category from the supplied use case.
            if area["status"] == "Not triggered by supplied use case":

                report_lines.append(
                    "No indicators for this assurance area were "
                    "identified from the supplied use-case information."
                )

            # If the assurance area was triggered but no evidence was
            # retrieved, I want to distinguish this from the category
            # simply being irrelevant.
            #
            # This also highlights a limitation of the current
            # keyword-based retrieval process.
            else:

                report_lines.append(
                    "This assurance area was identified as relevant, "
                    "but supporting evidence was not retrieved by the "
                    "current keyword-based retrieval process."
                )

        report_lines.append("")

    # ---------------------------------------------------------
    # PROTOTYPE LIMITATIONS
    # ---------------------------------------------------------
    #
    # I want the prototype to be explicit about what it can and
    # cannot currently do.
    #
    # This is particularly important for an AI assurance tool,
    # where automated output should not be treated as a substitute
    # for appropriate professional and human review.

    report_lines.append("## Prototype Limitations")
    report_lines.append("")

    report_lines.append(
        "- Assurance areas are currently identified using transparent "
        "rule-based indicators rather than a trained AI classifier."
    )

    report_lines.append(
        "- Retrieval currently uses keyword matching rather than "
        "semantic embeddings."
    )

    report_lines.append(
        "- Relevant policy material may therefore be missed if the "
        "terminology in the use case differs from the terminology "
        "used in the framework."
    )

    report_lines.append(
        "- Retrieved evidence may include sections that are only "
        "partially relevant to the use case."
    )

    report_lines.append(
        "- Recommended actions are generated using predefined "
        "rule-based guidance rather than a language model."
    )

    report_lines.append(
        "- The prototype identifies areas requiring consideration; "
        "it does not determine whether an AI system is safe, compliant "
        "or suitable for deployment."
    )

    report_lines.append(
        "- Findings should be reviewed by appropriately qualified "
        "technical, governance, legal, privacy and security specialists "
        "where relevant."
    )

    report_lines.append("")

    # Join all of the individual report lines together into
    # one Markdown document.
    return "\n".join(report_lines)


def save_report(report_text, assessment):
    """
    Save the generated assessment into the project's outputs folder.

    I want each assessment to have a filename based on the organisation
    being assessed rather than using one hard-coded filename.

    This means I can run the prototype for different organisations
    without automatically overwriting previous reports.
    """

    # Point to the folder where generated reports will be stored.
    output_directory = Path("outputs")

    # Create the folder if it does not already exist.
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Convert the agency name into a simple filename.
    #
    # For example:
    #
    # "Western Power"
    #
    # becomes:
    #
    # "western_power_ai_assessment.md"
    agency_name = (
        assessment["agency"]
        .lower()
        .strip()
        .replace(" ", "_")
    )

    filename = (
        f"{agency_name}_ai_assessment.md"
    )

    output_path = (
        output_directory
        / filename
    )

    # Save the Markdown report using UTF-8 encoding.
    output_path.write_text(
        report_text,
        encoding="utf-8",
    )

    return output_path


# ---------------------------------------------------------
# GENERATE THE SAMPLE REPORT
# ---------------------------------------------------------
#
# I only want to generate and save the sample report when I
# execute this file directly.
#
# The functions above can also be imported and reused by
# run_assessment.py for completely different agency scenarios.


if __name__ == "__main__":

    # Convert the structured assessment into a readable report.
    report = generate_markdown_report(
        assessment
    )

    # Save the completed report to the outputs folder.
    output_path = save_report(
        report,
        assessment,
    )

    # Confirm where the report was created.
    print("\nAssessment report generated successfully.")
    print(f"Saved to: {output_path}")
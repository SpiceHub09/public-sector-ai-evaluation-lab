from chunk_document import chunks
from evaluate_use_case import gather_policy_evidence
from assess_use_case import (
    identify_relevant_categories,
    classify_evidence,
    build_assessment,
)
from generate_report import generate_markdown_report, save_report


def get_use_case_from_user():
    """
    Collect information about an AI use case from the person
    running the prototype.

    Until now, I've used a hard-coded health-sector example to
    develop and test the assessment pipeline.

    I now want the same prototype to work with different AI problems
    from different agencies without changing the source code each time.

    This makes the tool more representative of a public-sector AI
    team that may need to work across very different agency problems.
    """

    print("\n" + "=" * 70)
    print("PUBLIC SECTOR AI EVALUATION LAB")
    print("=" * 70)

    print(
        "\nEnter some basic information about the AI use case "
        "you want to assess.\n"
    )

    # Ask the user which organisation or agency is considering
    # the AI solution.
    agency = input(
        "Agency or organisation: "
    ).strip()

    # Ask for a short description of the AI technology or system.
    ai_system = input(
        "AI system or solution: "
    ).strip()

    # Ask what problem the organisation wants the AI system to solve.
    purpose = input(
        "Purpose of the AI system: "
    ).strip()

    # Ask what type of information the system will process.
    #
    # This may later help the prototype identify privacy,
    # security and data-governance considerations.
    data = input(
        "Data used by the AI system: "
    ).strip()

    # Ask the user to describe any risks or concerns they already
    # know may be relevant.
    #
    # For V1, these terms also help guide the keyword-based
    # retrieval process.
    concerns = input(
        "Known concerns or risks: "
    ).strip()

    # Store the answers using the same structure as the original
    # health-sector test scenario.
    #
    # This means I can reuse the retrieval and assessment functions
    # I've already built without rewriting them.
    use_case = {
        "agency": agency,
        "ai_system": ai_system,
        "purpose": purpose,
        "data": data,
        "concerns": concerns,
    }

    return use_case


def run_assessment(use_case):
    """
    Run the complete assurance pipeline for a new AI use case.

    This connects the separate components I've developed so far:

    1. retrieve relevant policy evidence,
    2. classify that evidence into assurance areas,
    3. build a structured assessment, and
    4. generate a readable report.
    """

    # Retrieve the parts of the government AI assurance framework
    # that appear most relevant to this use case.
    evidence = gather_policy_evidence(
        use_case=use_case,
        policy_chunks=chunks,
    )

    # Group the retrieved evidence into the assurance categories
    # used by the prototype.
    # First, identify which assurance areas are relevant based on
    # the characteristics and concerns of the actual use case.
    relevant_categories = identify_relevant_categories(
    use_case
)

    # Then look for government policy evidence supporting those
        # identified assurance areas.
    categories = classify_evidence(
        evidence,
        relevant_categories,
)

    # Build the structured assessment, including status,
    # recommendations and supporting policy evidence.
    assessment = build_assessment(
        use_case=use_case,
        categories=categories,
    )

    return assessment


# ---------------------------------------------------------
# RUN THE COMPLETE PROTOTYPE
# ---------------------------------------------------------


if __name__ == "__main__":

    # Collect a new AI scenario from the user.
    use_case = get_use_case_from_user()

    print("\nAssessing use case...")

    # Run the scenario through the complete assessment pipeline.
    assessment = run_assessment(
        use_case
    )

    # Turn the structured result into a Markdown report.
    report = generate_markdown_report(
        assessment
    )

    # Save the report into the outputs folder.
    output_path = save_report(
        report,
        assessment,
)

    # Give the user a short summary of what the prototype found.
    print("\n" + "=" * 70)
    print("ASSESSMENT COMPLETE")
    print("=" * 70)

    print(
        f"\nAgency: {assessment['agency']}"
    )

    print(
        f"AI system: {assessment['ai_system']}"
    )

    print("\nAssurance areas:")

    for area in assessment["assurance_areas"]:
        print(
            f"  - {area['category']}: "
            f"{area['status']}"
        )

    print(
        f"\nReport saved to: {output_path}"
    )
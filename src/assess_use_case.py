from evaluate_use_case import use_case, evidence


def identify_relevant_categories(use_case):
    """
    Identify which assurance areas are relevant to the AI use case.

    In my earlier version, I classified assurance areas only after
    retrieving policy evidence.

    Testing the prototype against different scenarios showed a
    limitation with that approach.

    For example, a user could explicitly identify "accuracy" as a
    concern, but if the initial retrieval did not return a policy
    chunk containing one of my reliability keywords, the prototype
    could incorrectly report that no reliability evidence was found.

    I now want the characteristics of the actual AI use case to help
    determine which assurance areas should be investigated.
    """

    # Combine the important information supplied about the use case
    # into one searchable string.
    use_case_text = (
        f"{use_case['ai_system']} "
        f"{use_case['purpose']} "
        f"{use_case['data']} "
        f"{use_case['concerns']}"
    ).lower()

    # Define indicators that suggest each assurance area may be
    # relevant to the proposed AI system.
    #
    # These are deliberately transparent rules for V1 so I can
    # explain exactly why an assurance area was triggered.
    category_rules = {
        "Privacy and security": [
            "privacy",
            "security",
            "personal",
            "sensitive",
            "confidential",
            "clinical",
            "patient",
        ],

        "Reliability and testing": [
            "accuracy",
            "reliability",
            "safety",
            "testing",
            "validation",
            "performance",
            "monitoring",
            "failure",
            "hallucination",
            "predict",
        ],

        "Human oversight": [
            "human oversight",
            "human review",
            "decision",
            "recommendation",
            "clinical",
            "safety",
            "high risk",
        ],

        "Accountability and governance": [
            "accountability",
            "governance",
            "risk",
            "responsibility",
            "deployment",
            "decision",
        ],

        "Transparency and explainability": [
            "transparency",
            "explainability",
            "explain",
            "decision",
            "recommendation",
            "predict",
        ],
    }

    relevant_categories = {}

    # Compare the use case against each assurance area's indicators.
    for category_name, indicators in category_rules.items():

        matched_indicators = [
            indicator
            for indicator in indicators
            if indicator in use_case_text
        ]

        # Only flag the category when the actual use case contains
        # an indicator suggesting that the area requires attention.
        if matched_indicators:
            relevant_categories[category_name] = {
                "matched_indicators": matched_indicators,
            }

    return relevant_categories


def classify_evidence(evidence, relevant_categories):
    """
    Match retrieved government guidance to the assurance areas
    already identified from the use case.

    This separates two questions:

    1. What risks or assurance areas appear relevant to this use case?
    2. What evidence does the government framework provide about them?

    Keeping those questions separate makes the assessment easier
    to explain and reduces the chance that an important user concern
    is ignored simply because retrieval missed a particular section.
    """

    categories = {
        "Privacy and security": {
            "keywords": [
                "privacy",
                "security",
                "personal information",
                "sensitive information",
                "data governance",
            ],
            "recommendation":
                "Review what information the AI system can access, "
                "whether personal or sensitive information may be processed, "
                "where prompts and responses are stored, and what security "
                "and access controls are required.",
        },

        "Reliability and testing": {
            "keywords": [
                "testing",
                "test",
                "verify",
                "validation",
                "performance",
                "reliable",
                "reliability",
                "monitor",
                "evaluate",
                "accuracy",
            ],
            "recommendation":
                "Define a structured testing approach before deployment. "
                "Test the system against representative questions and edge "
                "cases, record incorrect or unsupported responses, establish "
                "acceptable performance criteria, and plan ongoing monitoring.",
        },

        "Human oversight": {
            "keywords": [
                "human oversight",
                "human accountability",
                "human feedback",
                "human validation",
            ],
            "recommendation":
                "Define where human review is required and make clear that "
                "users remain responsible for verifying important AI-generated "
                "outputs against authoritative source information.",
        },

        "Accountability and governance": {
            "keywords": [
                "accountability",
                "accountable",
                "governance",
                "risk management",
                "roles and responsibilities",
            ],
            "recommendation":
                "Establish clear ownership for the AI system, including who "
                "approves its use, who manages risks, who responds to incidents, "
                "and how the system fits within existing governance and risk "
                "management processes.",
        },

        "Transparency and explainability": {
            "keywords": [
                "transparency",
                "explainability",
                "explanation",
                "explain",
                "records",
            ],
            "recommendation":
                "Document how the AI system works, what information it uses, "
                "its known limitations, the results of testing, and when users "
                "should independently verify an output.",
        },
    }

    # Prepare each assurance category for assessment.
    for category_name, category_details in categories.items():

        category_details["evidence"] = []

        # Record whether the actual use case triggered this category.
        if category_name in relevant_categories:

            category_details["relevant_to_use_case"] = True

            category_details["matched_indicators"] = (
                relevant_categories[category_name]["matched_indicators"]
            )

        else:

            category_details["relevant_to_use_case"] = False
            category_details["matched_indicators"] = []

    # Work through the retrieved policy evidence.
    for result in evidence:

        text = result["text"].lower()

        # Only look for supporting evidence for assurance categories
        # that the use case itself has indicated may be relevant.
        for category_name, category_details in categories.items():

            if not category_details["relevant_to_use_case"]:
                continue

            matched_keywords = [
                keyword
                for keyword in category_details["keywords"]
                if keyword in text
            ]

            # If relevant policy terminology appears in this chunk,
            # retain the source information and the concepts that matched.
            if matched_keywords:

                category_details["evidence"].append(
                    {
                        "page_number": result["page_number"],
                        "chunk_number": result["chunk_number"],
                        "matched_keywords": matched_keywords,
                        "text": result["text"],
                    }
                )

    return categories


def build_assessment(use_case, categories):
    """
    Build the final structured assurance assessment.

    I distinguish between:

    - an assurance area that was triggered by the use case and has
      supporting policy evidence,

    - an assurance area that appears relevant but where the current
      retrieval process did not find supporting evidence, and

    - an assurance area that was not triggered by the information
      supplied about the use case.

    This gives the output more meaning than simply marking every
    category as requiring review.
    """

    assessment = {
        "agency": use_case["agency"],
        "ai_system": use_case["ai_system"],
        "purpose": use_case["purpose"],
        "assurance_areas": [],
    }

    # Work through each assurance category and assign a status.
    for category_name, category_details in categories.items():

        if category_details["relevant_to_use_case"]:

            # The use case indicates that this assurance area matters,
            # and relevant policy evidence has also been retrieved.
            if category_details["evidence"]:
                status = "Review required"

            # The use case indicates that this area matters, but the
            # current retrieval process did not find supporting evidence.
            #
            # I deliberately keep this separate from "not relevant"
            # because failure to retrieve evidence does not mean the
            # assurance issue can be ignored.
            else:
                status = "Relevant - evidence not retrieved"

        else:

            # Based on the information supplied by the user, this
            # assurance area was not triggered by the current V1 rules.
            status = "Not triggered by supplied use case"

        assessment["assurance_areas"].append(
            {
                "category": category_name,
                "status": status,
                "matched_indicators":
                    category_details["matched_indicators"],
                "recommendation":
                    category_details["recommendation"],
                "evidence":
                    category_details["evidence"],
            }
        )

    return assessment


# ---------------------------------------------------------
# SAMPLE HEALTH-SECTOR ASSESSMENT
# ---------------------------------------------------------
#
# I keep the original health scenario available as a test case.
#
# The reusable functions above can also work with completely
# different scenarios entered through run_assessment.py.


# First, identify which assurance categories appear relevant
# to the sample health-sector use case.
relevant_categories = identify_relevant_categories(
    use_case
)

# Next, examine the retrieved government guidance for evidence
# supporting those identified assurance categories.
categories = classify_evidence(
    evidence,
    relevant_categories,
)

# Finally, build the structured assessment.
assessment = build_assessment(
    use_case,
    categories,
)


# ---------------------------------------------------------
# TEST THE ASSESSMENT
# ---------------------------------------------------------
#
# I only want this detailed preview to appear when I execute
# assess_use_case.py directly.
#
# Other parts of the application can import the reusable functions
# and assessment data without printing this test output.


if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("AI ASSURANCE ASSESSMENT")
    print("=" * 70)

    print(f"\nAgency: {assessment['agency']}")
    print(f"AI system: {assessment['ai_system']}")
    print(f"Purpose: {assessment['purpose']}")

    for area in assessment["assurance_areas"]:

        print("\n" + "-" * 70)

        print(f"Assurance area: {area['category']}")
        print(f"Status: {area['status']}")

        # Show which characteristics of the use case caused this
        # assurance area to be triggered.
        if area["matched_indicators"]:
            print(
                "Use-case indicators: "
                + ", ".join(area["matched_indicators"])
            )

        # Only display a recommended action when the assurance area
        # was actually triggered by the supplied use case.
        if area["status"] != "Not triggered by supplied use case":

            print("\nRecommended action:")
            print(area["recommendation"])

        # Show any supporting policy evidence retrieved for
        # the assurance area.
        if area["evidence"]:

            print("\nPolicy evidence:")

            for item in area["evidence"]:

                print(
                    f"  - Page {item['page_number']}, "
                    f"Chunk {item['chunk_number']} | "
                    f"Matched: "
                    f"{', '.join(item['matched_keywords'])}"
                )

        # If the category was triggered but the retrieval stage
        # found no evidence, state that explicitly.
        elif area["status"] != "Not triggered by supplied use case":

            print(
                "\nPolicy evidence: none retrieved by "
                "the current retrieval process"
            )
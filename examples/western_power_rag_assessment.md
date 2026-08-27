# Public Sector AI Assurance Assessment

**Assessment method:** Semantic retrieval + evidence-grounded LLM analysis

## AI Use Case

**Agency:** Western Power

**AI system:** AI model that predicts potential failures in electricity network assets

## Initial Assessment

The evidence indicates that Western Power's asset failure prediction model operates in a context with safety and reliability implications. To ensure safe and responsible deployment, the agency should establish proportionate governance, maintain strong data quality, train staff to exercise judgment and avoid overreliance, establish monitoring loops, and consider alignment with relevant AI standards.

## Assurance Findings

### 1. Governance and Risk Management

**Finding:** The AI model is used in a domain context where false predictions or failure to predict network asset issues present safety and reliability concerns, indicating a potential high-risk setting.

**Why it matters:** The framework indicates that AI use should be assessed and managed on a case-by-case basis. High-risk settings warrant oversight mechanisms and proportionate governance to manage risks throughout the system lifecycle.

**Recommended action:** The agency should adapt decision-making structures, conduct lifecycle risk self-assessments, and consider establishing oversight bodies or AI risk committees to provide expert advice.

**Supporting framework evidence:**

**Page 11, Chunk 1**

> 8National framework for the assurance of artificial intelligence in government Cornerstones of assurance A risk-based approach The use of AI should be assessed and managed on a case-by-case basis. This ensures safe and responsible development, procurement and deployment in high- risk settings, with minimal administrative burden in lower-risk settings. The level of risk depends on the specifics of each case, including factors such as the business domain context and data characteristics. Self-assessment models, such as the NSW Artificial Intelligence Assurance Framework, help to identify, assess, document and manage these risks. Risks should be managed throughout the AI system lifecycle, including reviews at transitions between lifecycle phases. The OECD defines the phases of an AI system as

**Page 11, Chunk 3**

> datasets, processes, and decisions based on the potential for harm. Monitoring and feedback loops should be established to address emerging risks, unintended consequences or performance issues. Plans should be made for risks presented by obsolete and legacy AI systems. Governments should also consider oversight mechanisms for high-risk settings, including but not limited to external or internal review bodies, advisory bodies or AI risk committees, to provide consistent, expert advice and recommendations.

**Page 10, Chunk 1**

> 7National framework for the assurance of artificial intelligence in government Cornerstones of assurance Existing decision-making and accountability structures should be adapted and updated to govern the use of AI. This reflects the likely impacts upon a range of government functions, allows for diverse perspectives, designates lines of responsibility and provides clear sight to agency leaders of the AI uses they are accountable for. Governance structures should be proportionate and adaptable to encourage innovation while maintaining ethical standards and protecting public interests. At the agency level, leaders should commit to the safe and responsible use of AI and develop a positive AI risk culture to make open, proactive AI risk management an intrinsic part of everyday work. They shoul

### 2. Data Governance

**Finding:** The model relies on historical asset condition, maintenance, and failure data to generate failure predictions.

**Why it matters:** The evidence highlights that the quality of an AI model's output is driven by the quality of its data, making reliable and authenticated data essential to prevent inaccurate predictions.

**Recommended action:** The agency should ensure datasets used for model training and operation are properly authenticated, managed, maintained, and verified for reliability.

**Supporting framework evidence:**

**Page 10, Chunk 2**

> responsible use of AI and develop a positive AI risk culture to make open, proactive AI risk management an intrinsic part of everyday work. They should provide the necessary information, training and resources for staff to have the knowledge and means to: • align with the government’s objectives • use AI ethically and lawfully • exercise discretion and judgement in using AI outputs • identify, report and mitigate risks • consider testing, transparency and accountability requirements • support the community through changes to public service delivery • clearly explain AI-influenced outcomes. Data governance The quality of an AI model’s output is driven by the quality of its data. It’s therefore important to create, collect, manage, use and maintain datasets that are authenticated, reliable,

### 3. Human Oversight and Staff Capability

**Finding:** Known concerns around false predictions and human oversight require staff to exercise discretion when using AI outputs for maintenance planning.

**Why it matters:** Governments remain responsible for AI outputs. Overreliance must be avoided, and staff need the training and discretion to exercise proper judgment regarding system limitations and outputs.

**Recommended action:** Provide training and clear procedures so staff understand system limitations, exercise independent judgment, and can escalate concerns or identified risks to accountable parties.

**Supporting framework evidence:**

**Page 28, Chunk 2**

> d other obligations • integration with existing governance and risk management frameworks. 8.2. Train staff and embed capability Governments should establish policies, procedures, and training to ensure all staff understand their duties and responsibilities, understand system limitations and implement AI assurance practices. 8.3. Embed a positive risk culture Governments should ensure a positive risk culture, promoting open, proactive AI risk management as an intrinsic part of everyday practice. This fosters open discussion of uncertainties and opportunities, encourages staff to express their concerns and maintains processes to escalate to the appropriate accountable parties. 8.4. Avoid overreliance Governments remain responsible for all outputs generated by AI systems and must ensure inco

**Page 10, Chunk 2**

> responsible use of AI and develop a positive AI risk culture to make open, proactive AI risk management an intrinsic part of everyday work. They should provide the necessary information, training and resources for staff to have the knowledge and means to: • align with the government’s objectives • use AI ethically and lawfully • exercise discretion and judgement in using AI outputs • identify, report and mitigate risks • consider testing, transparency and accountability requirements • support the community through changes to public service delivery • clearly explain AI-influenced outcomes. Data governance The quality of an AI model’s output is driven by the quality of its data. It’s therefore important to create, collect, manage, use and maintain datasets that are authenticated, reliable,

### 4. System Monitoring and Standards Alignment

**Finding:** Ongoing performance and unintended consequences of failure predictions require continuous tracking, and alignment with recognized standards should be considered.

**Why it matters:** Monitoring and feedback loops help address emerging performance issues or unintended consequences, while alignment with standards supports consistent and safe implementation.

**Recommended action:** Establish monitoring and feedback loops for prediction accuracy and consider aligning AI governance and risk management with standards such as AS ISO/IEC 42001:2023 or AS ISO/IEC 23894:2023 where practical.

**Supporting framework evidence:**

**Page 11, Chunk 3**

> datasets, processes, and decisions based on the potential for harm. Monitoring and feedback loops should be established to address emerging risks, unintended consequences or performance issues. Plans should be made for risks presented by obsolete and legacy AI systems. Governments should also consider oversight mechanisms for high-risk settings, including but not limited to external or internal review bodies, advisory bodies or AI risk committees, to provide consistent, expert advice and recommendations.

**Page 12, Chunk 1**

> 9National framework for the assurance of artificial intelligence in government Cornerstones of assurance Standards Where practical, governments should align their approaches to relevant AI standards. Standards outline specifications, procedures, and guidelines to enable the safe, responsible, consistent, and effective implementation AI in a consistent and interoperable manner. Some current AI governance and management standards include: • AS ISO/IEC 42001:2023 Information technology - Artificial intelligence - Management system • AS ISO/IEC 23894:2023 Information technology - Artificial intelligence - Guidance on risk management • AS ISO/IEC 38507:2022 Information technology - Governance of IT - Governance implications of the use of artificial intelligence by organizations Governments shou

## Further Review

- Further review is appropriate to examine the specific authentication and quality controls applied to historical maintenance and failure datasets (page_10_chunk_2).
- Further review is recommended regarding the specific human-in-the-loop procedures and staff training established to avoid overreliance on automated failure predictions (page_28_chunk_2, page_10_chunk_2).
- Further assessment is suggested to determine whether formal internal/external AI risk committees or advisory bodies have been established for this system (page_11_chunk_3).
- Further review should evaluate the ongoing feedback and monitoring mechanisms designed to capture false predictions or unintended performance issues (page_11_chunk_3).

## Important Note

This is an exploratory AI-assisted assessment. Semantic retrieval and language-model analysis can miss, misinterpret or overstate relevant guidance. The included source evidence is provided to support human verification of generated findings. The output should not be treated as a compliance, legal or deployment decision.

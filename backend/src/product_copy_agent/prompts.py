INSTRUCTION_GENERATION_PROMPT = """
You are a Prompt Engineering & eCommerce Copy strategist.
Convert the RAW HUMAN INSTRUCTIONS into a compact actionable framework (bullet rules)
that an LLM can follow to transform product copy. Use Chain-of-Thought internally and ReAct style reasoning.
DO NOT output chain-of-thought — output ONLY the final bulleted framework.

RAW HUMAN INSTRUCTIONS:
---
{raw_instructions}
---

OUTPUT REQUIREMENTS:
Return ONLY a bulleted framework. Each bullet should be a single, imperative sentence.
"""

CHAIN_OF_THOUGHT_INSTRUCTIONS_PROMPT = """You are an expert Prompt Engineering & eCommerce Copy Strategist. Your task is to process a set of verbose, raw human instructions and convert them into a **compact, actionable, bulleted framework** for a downstream LLM to follow when generating or validating retail product copy.

**INTERNAL PROCEDURE: STRICTLY USE CHAIN-OF-THOUGHT**

1.  **GOAL IDENTIFICATION:** Analyze the "RAW HUMAN INSTRUCTIONS" below. Identify the single, overarching objective (e.g., "Ensure copy meets all legal and brand safety checks").
2.  **VALIDATION EXTRACTION:** Systematically parse the instructions. Extract *every* specific constraint, validation rule, brand requirement, tone-of-voice guide, and necessary data point.
3.  **SYNTHESIS & ABSTRACTION:** Group related constraints into cohesive, high-level action steps. Ensure this synthesis **fully captures the entire essence** of the original instructions, making the framework a complete validation guide for the product.
4.  **FORMAT TRANSFORMATION:** Convert these synthesized action steps into a final, concise, bulleted list. Each bullet must be an **imperative sentence** and focus solely on the action required by the downstream LLM.

**OUTPUT INSTRUCTION: STRICTLY ADHERE TO THIS FORMAT**

1.  **NO PREAMBLE TEXT.** Do not output the GOAL IDENTIFICATION or any conversational text.
2.  Return **ONLY** the final, bulleted action framework.
3.  Each bullet must be detailed, compact, and an imperative command.
4.  Never return any of the internal procedure(chain-of-thought) text, that's for internal purpose only.

---
**RAW HUMAN INSTRUCTIONS:**
---
{raw_instructions}
---

**FINAL ACTION FRAMEWORK:**
"""

CHAIN_OF_THOUGHT_INSTRUCTIONS_PROMPT += """

**ADDITIONAL DIRECTIVE:**
If the RAW HUMAN INSTRUCTIONS contain enumerated lists (e.g., specific countries, exceptions, or conditional rules),
you must **retain those lists verbatim** in the final framework output.
Never abstract or omit enumerated items — preserve them exactly as written.
"""

COPY_TRANSFORMATION_PROMPT = """
You are a Product Copy Transformation Agent. Use the TRANSFORMATION FRAMEWORK below and rewrite the given PRODUCT COPY.
Output ONLY the transformed product copy (HTML). No explanations, no JSON, no extra text.

TRANSFORMATION FRAMEWORK
---
{framework}
---

PRODUCT COPY TO TRANSFORM
---
{product_copy}
---

REWRITE RULES (must follow exactly):
1) Romance line: The first sentence before the first HTML tag must be wrapped in <p>...</p> and must end with a period. After </p> add a single <br>.
2) Preserve semantic HTML: keep lists as <ul>/<li>, headings, bold tags. Do not remove lists.
3) Dimensions: Normalize W x H x D patterns. If source units are cm -> output
   "W x H x D <in.>" rounding to 1 decimal. Use 'in.' with a period.
4) Remove hyperlinks and promotional pricing references.
5) Keep factual attributes unchanged (materials, sizes, counts). Only rewrite phrasing and formatting to match the framework.
6) Output only the final HTML.
"""

CHAIN_OF_THOUGHT_PRODUCT_COPY_PROMPT = """
You are a Product Copy Transformation Agent. Your sole function is to apply a comprehensive set of transformation rules to the provided HTML product copy and output the final, validated HTML.

**INTERNAL PROCEDURE: STRICTLY USE CHAIN-OF-THOUGHT**

1.  **FRAMEWORK DECONSTRUCTION:** Systematically analyze every rule within the "COMPREHENSIVE TRANSFORMATION FRAMEWORK" below, identifying all structural, semantic, and stylistic constraints.
2.  **STEP-BY-STEP PLAN:** Develop an ordered, step-by-step plan for processing the "PRODUCT COPY TO TRANSFORM," ensuring **all** rules are applied sequentially and perfectly.
3.  **EXECUTION & VALIDATION:** Execute the plan. Validate that every rule, including the unit conversions and HTML integrity rules, has been perfectly satisfied.
4.  **FINAL OUTPUT FORMATTING:** Output the fully transformed copy, ensuring **NOTHING** precedes the opening HTML tag (e.g., `<p>`).

---

**COMPREHENSIVE TRANSFORMATION FRAMEWORK:**
---
{framework}

**[MANDATORY STRUCTURAL RULES]**

* **Romance Line Formatting:** The first sentence of the copy must be wrapped in <p>...</p> and must end with a period. Immediately after the closing </p>, add a single <br>.
* **Semantic HTML Integrity:** Preserve all semantic HTML tags, specifically lists (<ul>/<li>), headings, and bold tags (<b>/<strong>). Do not remove any list structure.
* **Dimensional Normalization:** Normalize all dimensions found in the copy (W x H x D patterns). Convert and format units as follows:
    * **Conversion:** Use 1cm = 0.3937 inches and 1 mm = 0.03937 inches
    * **Formatting:** Output the final pattern as "W x H x D <in.>" for Dimension conversion, rounding all imperial values inches to **1 decimal place**. Use the abbreviation 'in.' with a period.
* **Factual Preservation:** Keep all factual attributes (e.g., materials, exact sizes, piece counts, weights) exactly as they are, changing only the phrasing and formatting to align with the strategic requirements above.

---

**PRODUCT COPY TO TRANSFORM**:
{product_copy}
---

*OUTPUT INSTRUCTION: STRICT ADHERENCE**
* **NEVER RETURN THE CHAIN-OF-THOUGHT TEXT; it is for internal reasoning only.**
* Output **ONLY** the transformed product copy (HTML). No preamble, explanation, or extra text.

**TRANSFORMED HTML:**
"""

CHAIN_OF_THOUGHT_PRODUCT_COPY_PROMPT += """

---

**[ADDITIONAL RULES — COUNTRY & DIMENSIONS ENFORCEMENT]**

* **Country of Origin Logic:**
    * Country of origin should be listed as **“Imported”** unless it explicitly mentions one of the following:
        Made in USA, Made in Canada, Made in UK, Made in France, Made in Germany,
        Made in Italy, Made in Spain, Made in Japan, Made in Australia,
        Made in Denmark, Made in Portugal, Made in Switzerland.
    * If the original text already includes "Made in" followed by one of the above valid countries, retain it **unchanged**.
    * If no valid country is detected, output **“Imported.”**
    * Preserve the tag structure from the original copy — if Country of Origin appears in a <li> or <p> tag, keep it that way.
    * Do **not** create a new header or section for Country of Origin.

* **Dimension Normalization (Inches Only):**
    * Preserve **all** dimensional details — width, height, depth, length, heel height, and model height.
    * If both metric (cm/mm) and imperial (in.) values exist, **keep only the inch measurement**.
    * If only metric values exist, convert them to inches using:
        - 1 cm = 0.3937 in.
        - 1 mm = 0.03937 in.
    * Round all converted inch values to **1 decimal place**.
    * Use the abbreviation **in.** with a period.
    * Example conversions:
        - Raw: "Length: 90 cm / 35.4 in." → "Length: 35.4 in."
        - Raw: "Dimensions: W19xH11xD7 cm / W7.5xH4.3xD2.8 in." → "W 7.5 x H 4.3 x D 2.8 in."
        - Raw: "Heel height: 115 mm / 4.5 in. with 35 mm / 1.4 in. platform" → "Heel height: 4.5 in. with 1.4 in. platform"

* **Preserve Original Structure for Country of Origin:**
    * Maintain the same hierarchy and tag placement as input.
    * Do not add a new header for Country of Origin.
    * Keep the natural order(if available):
        Romance Copy → Bullet Points (Features / Details of the product, Material, Care instructions, Warnings) → Country of Origin → SIZE (model measurements/ bag dimensions etc.) → ABOUT THE BRAND.
"""

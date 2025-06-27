from langchain_core.prompts import PromptTemplate

image_product_details_prompt = """
        "Analyze the product image and return structured product details strictly as raw JSON (do not include markdown or code formatting). "
        "Use this exact structure:\n"
        "{\n"
        "\"product_name\" (product name),\n"
        "\"description\" (short marketing-friendly description),\n"
        "\"key_benefits\" (list of 3–5 standout benefits),\n"
        "\"hashtags\" (list of 4 hastags),\n"
        "\"price\" (estimated price if visible or appropriate otherwise low and exciting prices),\n"
        "\"offer\" (any promotional offer if implied or suggest a generic one).\n"
        "}\n"
        "Values should be marketing-ready and descriptive.

        IMPORTANT:
        - Do not include any text before or after the JSON.
        - Do not wrap the JSON in quotes.
        - Do not add markdown syntax (like ``` or ```json).
        - Respond only with Dictionary.
        """




text_product_detail_prompt = """
Analyze the following official medication guide or prescribing information, 
and extract marketing-ready information strictly as dictionary type 
(do not include markdown or code formatting)
to support the creation of compliant advertisements across digital platforms.

The dictionary may contain the following keys:


- "product_name": Full name of the drug including active ingredient and brand (e.g., "ABRILADA (adalimumab-afzb)")
- "generic_name": The active ingredient's name
- "manufacturer": The name of drug manufacturer
- "type": Classification or type of drug (e.g., biosimilar, TNF blocker, biologic)
- "fda_approved_uses": A list of clearly summarized, FDA-approved indications
- "key_benefits": A list of marketing-relevant benefits (e.g., at-home use, convenient dosing, biosimilar to well-known drug)
- "storage_handling": A short summary of storage or handling advantages, if any
- "support_programs": Any patient support, affordability, or access programs offered by the manufacturer
- "dosage_forms": List of all available dosage forms and strengths
- "patient_support" : list of injection guide and support programs offered by the manufacturer
- "disclaimer" :  a concise disclaimer
- "hashtags": list of hastags for twitter,

    Return Strictly only Dictionary, without any explanation or extra formatting.

IMPORTANT:
    - Do not include any text before or after the JSON.
    - Do not wrap the JSON in quotes.
    - Do not add markdown syntax (like ``` or ```json).
    - Respond Strictly only with Dictionary.
        """





market_content_prompt_template = """
    Generate {user_type}-friendly marketing content in {language} language for {product_name} with the following requirements:

    Create EXACTLY TWO distinct marketing options with these IDs: {option_ids}
    Generated content should have high Bert Score.

    Follow these specific instructions:
    {platform_instructions}

        Product Details:
        - Name: {product_name}
        - Key Benefits: {key_benefits}
        - FDA Uses: {fda_uses}
        - Suggested Hashtags: {hashtags}

    Respond Strictly ONLY with Dictionary (no markdown, no code blocks, no explanations).

    IMPORTANT:
    - Do not include any text before or after the JSON.
    - Do not wrap the JSON in quotes.
    - Do not add markdown syntax (like ``` or ```json).
    - Respond Strictly only with Dictionary.

    expected language : {language}
    Here is the expected schema for the response:
    {platform_instructions}

    """



template = "Concise the content to keep token count under 70:\n\n{content}"







import ollama
import requests
from bs4 import BeautifulSoup
from PIL import Image
import base64
from io import BytesIO
import json
import uuid
from app.prompts.content import  image_product_details_prompt, text_product_detail_prompt
from langchain_core.prompts import PromptTemplate
from app.schemas.response import FacebookOutputModel, EmailOutputModel, BannerOutputModel
from app.helpers.validate import validate_response


def scrap_content(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers= headers)
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find_all('div', class_="Section")
    return content

def encode_image(image: Image.Image) -> str:
    buffered = BytesIO()
    # image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def generate_with_ollama(prompt, content=None):
    messages = [{"role": "user", "content": prompt}]

    response = ollama.chat(
        model='qwen2.5vl:3b',  # or other vision model available in Ollama
        messages=messages
    )
    return response['message']['content']


def generate_content_from_text(url, selected_sections: str, language: str, user_type: str = 'consumer'):
    # ... (existing scraping/product_details code) ...
    content = scrap_content(url)
    product_details = generate_with_ollama(text_product_detail_prompt, content)
    product_details = json.loads(product_details)

    # Generate two unique option IDs
    option_ids = [str(uuid.uuid4())[:30] for _ in range(2)]


    section_prompts = {
        "facebook": FacebookOutputModel,
        "email": EmailOutputModel,
        "banner": BannerOutputModel,
    }

    # selected_schemas = [section_prompts[s] for s in selected_sections]  -> for multiple values
    platform_instructions = section_prompts[selected_sections].model_json_schema()

    prompt_template = """
    Generate {user_type}-friendly marketing content in {language} language for {product_name} with the following requirements:

    Create EXACTLY TWO distinct marketing options with these IDs: {option_ids}

    Follow these specific instructions:
    {platform_instructions}

        Product Details:
        - Name: {product_name}
        - Key Benefits: {key_benefits}
        - FDA Uses: {fda_uses}
        - Suggested Hashtags: {hashtags}

    Respond Strictly ONLY with Dictionary (no markdown, no code blocks, no explanations).

    expected language : {language}
    Here is the expected schema for the response:
    {platform_instructions}

    IMPORTANT:
    - Do not include any text before or after the JSON.
    - Do not wrap the JSON in quotes.
    - Do not add markdown syntax (like ``` or ```json).
    - Respond Strictly only with Dictionary.

    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["product_name", "key_benefits", "fda_uses", "hashtags"],
        partial_variables={
            "option_ids": ", ".join(option_ids),
            "platform_instructions": platform_instructions,
            # "Platform_type" : selected_sections,
            "user_type": user_type,
            "format_instructions": section_prompts,
            "language": language
        }
    )

    formatted_prompt = prompt.format(
        product_name=product_details['product_name'],
        key_benefits=", ".join(product_details['key_benefits']),
        fda_uses=", ".join(product_details['fda_approved_uses']),
        hashtags=", ".join(product_details['hashtags'])
    )

    # Get LLM response
    response = generate_with_ollama(formatted_prompt)

    # convert to dict
    response_dict = json.loads(response)

    # validate the llm response
    validated_result = validate_response(response, section_prompts[selected_sections])

    # Now you can access validated_result.output[0].shortForm.headline, etc.
    final_response = validated_result.model_dump()

    return final_response, content




def generate_content_from_image(image, selected_sections: str, language :str, user_type: str = 'consumer'):
    # ... (existing scraping/product_details code) ...
    image_base64 = encode_image(image)

    product_details = generate_with_ollama(image_product_details_prompt, image_base64)
    product_details = json.loads(product_details)

    # Generate two unique option IDs
    option_ids = [str(uuid.uuid4())[:30] for _ in range(2)]

    section_prompts = {
        "facebook": FacebookOutputModel,
        "email": EmailOutputModel,
        "banner": BannerOutputModel,
    }

    # selected_schemas = [section_prompts[s] for s in selected_sections]  -> for multiple values
    platform_instructions = section_prompts[selected_sections].model_json_schema()


    prompt_template = """
        Generate {user_type}-friendly marketing content in {language} language for {product_name} with the following requirements:

        Create EXACTLY TWO distinct marketing options with these IDs: {option_ids}

        Follow these specific instructions:
        {platform_instructions}

            Follow these specific instructions:
    {platform_instructions}

        Product Details:
        - Name: {product_name}
        - Descrption: {description}
        - Key Benefits: {key_benefits}
        - Suggested Hashtags: {hashtags}
        - Price : {price}
        - Offer : {offer}

    Values should be marketing-ready and descriptive.
    Respond Strictly ONLY with Dictionary  (no markdown, no code blocks, no explanations).

    expected language : {language}
    Here is the expected schema for the response:
    {platform_instructions}

    IMPORTANT:
    - Respond only with the Dictionary.
    - Do not include any text before or after the JSON.
    - Do not wrap the JSON in quotes.
    - Do not add markdown syntax (like ``` or ```json).
    - Respond only with the Dictionary.
    
    """


    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["product_name", "description", "key_benefits", "hashtags", "price", "offer"],
        partial_variables={
            "option_ids": ", ".join(option_ids),
            "platform_instructions": platform_instructions,
            # "Platform_type" : selected_sections,
            "user_type": user_type,
            "format_instructions": section_prompts,
            "language": language
        }
    )

    formatted_prompt = prompt.format(
        product_name=product_details['product_name'],
        description=product_details['description'],
        key_benefits=", ".join(product_details['key_benefits']),
        price=(product_details['price']),
        hashtags=", ".join(product_details['hashtags']),
        offer=product_details['offer']
    )

    # Get LLM response
    response = generate_with_ollama(formatted_prompt)

    # convert to dict
    response_dict = json.loads(response)
    response_dict = {
        "facebook": response_dict.get("facebook", {}),
        "email": response_dict.get("email", {}),
        "banner": response_dict.get("banner", {})
    }


    # validate the llm response
    validated_result = validate_response(response, section_prompts[selected_sections])

    # Now you can access validated_result.output[0].shortForm.headline, etc.
    final_response = validated_result.model_dump()

    return final_response


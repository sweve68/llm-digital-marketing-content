import streamlit as st
from PIL import Image
from io import BytesIO
from app.helpers.file_content import generate_content_from_text,generate_content_from_image
from fastapi import APIRouter, File, UploadFile

from app.schemas.request import InputRequestText, InputRequestImage

router = APIRouter()

from fastapi import Form

@router.post("/digital/image")
async def get_digital_content_from_image(
    image: UploadFile = File(...),
    channel: str = Form(...),
    language: str = Form(...),
    audience: str = Form(...)
):
    try:
        # Read image
        image_bytes = await image.read()
        image = Image.open(BytesIO(image_bytes))

        # Clean inputs
        selected_sections = channel.lower()
        language = language.lower()
        audience = audience.lower()

        marketing_content = generate_content_from_image(image, selected_sections, language, audience)
        return {'output': marketing_content}
    except Exception as e:
        return {"error": str(e)}




@router.post("/digital/text")
async def get_digital_content_from_text(
    url: str = Form(...),
    channel: str = Form(...),
    language: str = Form(...),
    audience: str = Form(...)
):
    try:

        # Clean inputs
        selected_sections = channel.lower()
        language = language.lower()
        audience = audience.lower()

        marketing_content = generate_content_from_image(url, selected_sections, language, audience)
        return {'output': marketing_content}
    except Exception as e:
        return {"error": str(e)}


# @router.post("/digital/image")
# async def get_digital_content_from_image(params : InputRequestImage ,image: UploadFile = File(...)):
#     try:
#         # Read the image files
#         image_bytes = await image.read()
#         image = Image.open(BytesIO(image_bytes))
#         selected_sections = params.channel.lower()
#         language = params.language.lower()
#         audience = params.audience.lower()
#
#         marketing_content = generate_content_from_image(image, selected_sections,language,audience)
#
#         return {'output': marketing_content}
#     except Exception as e:
#         st.error(f"Error processing the image: {e}")
#         return {"error": str(e)}



@router.get("/digital/text/{platform}/{language}")
async def get_digital_content_from_text(params: InputRequestText):
    try:
        selected_sections = params.channel.lower()
        language = params.language.lower()
        audience = params.audience.lower()
        marketing_content = generate_content_from_text(params.url, selected_sections,language)
        return {'output': marketing_content}
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return {"error": str(e)}

#
# @router.post("/digital/image/{platform}/{language}")
# async def get_digital_content_from_image(params: InputRequestImage, image: UploadFile = File(...)):
#     try:
#         # Read the image files
#         image_bytes = await image.read()
#         image = Image.open(BytesIO(image_bytes))
#         selected_sections = params.platform.lower()
#         language = params.language.lower()
#         audience = params.audience.lower()
#
#         marketing_content = generate_content_from_image(image, selected_sections,language)
#
#         return {'output': marketing_content}
#     except Exception as e:
#         st.error(f"Error processing the image: {e}")
#         return {"error": str(e)}
#
#
#
# @router.get("/digital/text/{platform}/{language}")
# async def get_digital_content_from_text(params: InputRequestText):
#     try:
#         selected_sections = params.channel.lower()
#         language = params.language.lower()
#         audience = params.audience.lower()
#         marketing_content = generate_content_from_text(params.url, selected_sections,language)
#         return {'output': marketing_content}
#     except Exception as e:
#         st.error(f"Error processing the image: {e}")
#         return {"error": str(e)}
#
#
#
#
#

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# Define FacebookPydantic models
class FormContent(BaseModel):
    headline: str = Field(description='Concise headline of the content')
    body: str = Field(description='60 words for shortForm and 250 words for longform')
    hashtags: List[str] = Field(description='List of relevant hashtags', min_length=2)


class Option(BaseModel):
    optionId: str = Field(description='Unique identifier for the option')
    shortForm: FormContent
    longForm: FormContent


# Define Email Pydantic models
class ModuleContent(BaseModel):
    optionId: str = Field(..., description="Unique identifier for the content option")
    header: str = Field(..., description="Main header of the module")
    subheader: str = Field(..., description="Subheader providing more context")
    body: str = Field(..., description="Body text with personalization support")
    bulletedCopy: List[str] = Field(..., min_length=2, description="List of bullet points")
    call_to_action: str = Field(..., description="Call to action encouraging user response")


# Define Banner Pydantic models
class FrameModel(BaseModel):
    id: str = Field(..., description="Unique id for each frame")
    body: str = Field(..., description="Concise body text")


class OutputContent(BaseModel):
    optionId: str = Field(..., description="Unique identifier for the content option")
    frames: List[FrameModel] = Field(..., description="List of frames")
    call_to_action: str = Field(..., description="Call to action encouraging user response")


class FacebookOutputModel(BaseModel):
    output: List[Option] = Field(description='List of marketing options', min_length=2)


class EmailOutputModel(BaseModel):
    generatedModuleContent: List[ModuleContent] = Field(..., description="List of generated module content", min_length=2)

class BannerOutputModel(BaseModel):
    output: List[OutputContent] = Field(..., description="List of output content", min_length=2)


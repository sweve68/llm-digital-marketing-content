from pydantic import BaseModel, Field


class InputRequestText(BaseModel):
    # optionId: str = Field(..., description="Unique identifier for the content option")
    url : str = Field(..., description="URL of the content to be processed")
    channel: str = Field(..., description="Platform name selected by user")
    language: str = Field(..., description="Language selected by user")
    audience: str = Field(..., description="Target audience for the content")


class InputRequestImage(BaseModel):
    # optionId: str = Field(..., description="Unique identifier for the content option")
    # selected_sections: str = Field(..., description="Platform name selected by user")
    channel: str = Field(..., description="Platform name selected by user")
    language: str = Field(..., description="Language selected by user")
    audience: str = Field(..., description="Target audience for the content")
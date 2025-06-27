from pydantic import BaseModel
from typing import Union
import json

# def dict_convertor(response: str):
#     # Convert JSON string response to dictionary format
#     response_dict = json.loads(response)
#
#     # Wrap the response in a dictionary with key "output"
#     wrapped_dict = {"output": response}
#     return response_dict


def validate_response(response, model: BaseModel):
    """
    Validate a response using the provided Pydantic model.

    Args:
        response (str | dict): JSON string or dictionary to validate.
        model (BaseModel): Pydantic model to validate against.

    Returns:
        Parsed and validated object (Pydantic model instance)
    """

    try:
        # If response is a string, parse it
        if isinstance(response, str):
            response = json.loads(response)

        # Validate using the provided model
        validated = model(**response)
        return validated

    except Exception as e:
        raise ValueError(f"Validation failed: {e}")

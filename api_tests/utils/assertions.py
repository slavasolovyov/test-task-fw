import json
from typing import Any
import requests
from pydantic import BaseModel, ValidationError


def assert_status_code(response: requests.Response, expected_status: int):
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, but got {response.status_code}. "
        f"Response: {response.text[:500]}"
    )


def assert_response_schema(response: requests.Response, model: BaseModel) -> BaseModel:
    try:
        response_data = response.json()
        parsed = model.model_validate(response_data)
        return parsed
    except json.JSONDecodeError as e:
        raise AssertionError(f"Response is not valid JSON: {str(e)}")
    except ValidationError as e:
        raise AssertionError(f"Response doesn't match schema: {e.json()}")


def assert_response_contains(response: requests.Response, key: str, value: Any = None):
    response_data = response.json()
    assert key in response_data, f"Response doesn't contain key '{key}'"
    
    if value is not None:
        assert response_data[key] == value, (
            f"Expected {key} to be {value}, but got {response_data[key]}"
        )

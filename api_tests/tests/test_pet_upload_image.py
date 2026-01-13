import pytest
from pathlib import Path

from api_tests.api.pet_client import PetClient
from api_tests.models.pet import Pet
from api_tests.models.api_response import ApiResponse
from api_tests.utils.assertions import assert_status_code, assert_response_schema


@pytest.mark.regression
class TestPetUploadImage:
    
    def test_upload_image_with_file(self, api_client: PetClient, sample_pet: Pet):
        add_response = api_client.add_pet(sample_pet)
        assert_status_code(add_response, 200)
        pet_id = add_response.json().get("id")
        
        image_path = Path(__file__).parent / "test_data" / "test_image.png"
        response = api_client.upload_image(
            pet_id=pet_id,
            file_path=str(image_path),
            additional_metadata="Test metadata"
        )
        assert_status_code(response, 200)
        api_response = assert_response_schema(response, ApiResponse)
        assert api_response.code == 200
    
    
    def test_upload_image_invalid_pet_id(self, api_client: PetClient):
        image_path = Path(__file__).parent / "test_data" / "test_image.png"
        response = api_client.upload_image(
            pet_id=999999090903123,
            file_path=str(image_path)
        )
        assert response.status_code in [404]

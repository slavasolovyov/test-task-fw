import pytest
from typing import List

from api_tests.api.pet_client import PetClient
from api_tests.models.pet import Pet, Category, Tag
from api_tests.models.api_response import ApiResponse
from api_tests.utils.assertions import assert_status_code, assert_response_schema

@pytest.mark.regression
class TestPetAPI:
    
    def test_add_pet(self, api_client: PetClient, sample_pet: Pet):
        response = api_client.add_pet(sample_pet)
        
        assert_status_code(response, 200)
        pet_response = assert_response_schema(response, Pet)
        assert pet_response.name == sample_pet.name
        assert pet_response.status == sample_pet.status
    
    def test_get_pet_by_id(self, api_client: PetClient, sample_pet: Pet):
        add_response = api_client.add_pet(sample_pet)
        assert_status_code(add_response, 200)
        pet_id = add_response.json().get("id")
        
        response = api_client.get_pet_by_id(pet_id)
        assert_status_code(response, 200)
        pet_response = assert_response_schema(response, Pet)
        assert pet_response.id == pet_id
        assert pet_response.name == sample_pet.name
    
    def test_get_pet_by_id_not_found(self, api_client: PetClient):
        response = api_client.get_pet_by_id(999999)
        assert_status_code(response, 404)
    
    def test_update_pet(self, api_client: PetClient, sample_pet: Pet):
        add_response = api_client.add_pet(sample_pet)
        assert_status_code(add_response, 200)
        pet_data = add_response.json()
        pet_id = pet_data.get("id")
        
        updated_pet = Pet(
            id=pet_id,
            name="Updated Dog Name",
            photoUrls=sample_pet.photoUrls,
            status="sold"
        )
        response = api_client.update_pet(updated_pet)
        assert_status_code(response, 200)
        
        get_response = api_client.get_pet_by_id(pet_id)
        updated_pet_response = assert_response_schema(get_response, Pet)
        assert updated_pet_response.name == "Updated Dog Name"
        assert updated_pet_response.status == "sold"
    
    def test_find_pets_by_status(self, api_client: PetClient, sample_pet: Pet):
        add_response = api_client.add_pet(sample_pet)
        assert_status_code(add_response, 200)
        
        response = api_client.find_pets_by_status(["available"])
        assert_status_code(response, 200)
        
        pets = response.json()
        assert isinstance(pets, list)
        if pets:
            assert any(pet.get("status") == "available" for pet in pets)
    
    
    def test_find_pets_by_tags(self, api_client: PetClient, sample_pet: Pet):
        add_response = api_client.add_pet(sample_pet)
        assert_status_code(add_response, 200)
        
        response = api_client.find_pets_by_tags(["test-tag"])
        assert_status_code(response, 200)
        
        pets = response.json()
        assert isinstance(pets, list)
    
    def test_update_pet_with_form(self, api_client: PetClient, sample_pet: Pet):
        add_response = api_client.add_pet(sample_pet)
        assert_status_code(add_response, 200)
        pet_id = add_response.json().get("id")
        
        response = api_client.update_pet_with_form(
            pet_id=pet_id,
            name="Form Updated Name",
            status="pending"
        )
        assert_status_code(response, 200)
        
        get_response = api_client.get_pet_by_id(pet_id)
        updated_pet = assert_response_schema(get_response, Pet)
        assert updated_pet.name == "Form Updated Name"
        assert updated_pet.status == "pending"
    
    def test_delete_pet(self, api_client: PetClient, sample_pet: Pet):
        add_response = api_client.add_pet(sample_pet)
        assert_status_code(add_response, 200)
        pet_id = add_response.json().get("id")
        
        response = api_client.delete_pet(pet_id)
        assert_status_code(response, 200)
        
        get_response = api_client.get_pet_by_id(pet_id)
        assert_status_code(get_response, 404)
    
    def test_delete_pet_not_found(self, api_client: PetClient):
        response = api_client.delete_pet(999999090903123)
        assert_status_code(response, 404)
    
    def test_find_pets_by_status_invalid_status(self, api_client: PetClient):
        """Test finding pets with invalid status value."""
        response = api_client.find_pets_by_status(["invalid_status_value"])
        assert_status_code(response, 200)
        pets = response.json()
        assert isinstance(pets, list)
        assert len(pets) == 0
    
    def test_update_pet_with_form_invalid_id(self, api_client: PetClient):
        response = api_client.update_pet_with_form(
            pet_id=999999999999,
            name="Invalid Pet",
            status="available"
        )
        assert_status_code(response, 404)
    
    def test_add_pet_missing_required_body(self, api_client: PetClient):
        invalid_data = None
        response = api_client.post("pet", json_data=invalid_data)
        assert_status_code(response, 405)
    
    def test_get_pet_by_id_invalid_format(self, api_client: PetClient):
        response = api_client.get("pet/invalid_id")
        assert_status_code(response, 404)
    
    @pytest.mark.smoke
    def test_pet_lifecycle(self, api_client: PetClient):
        new_pet = Pet(
            name="Lifecycle Test Pet",
            photoUrls=["https://example.com/photo.jpg"],
            status="available"
        )
        create_response = api_client.add_pet(new_pet)
        assert_status_code(create_response, 200)
        pet_id = create_response.json().get("id")
        
        read_response = api_client.get_pet_by_id(pet_id)
        assert_status_code(read_response, 200)
        pet = assert_response_schema(read_response, Pet)
        assert pet.name == "Lifecycle Test Pet"
        
        updated_pet = Pet(
            id=pet_id,
            name="Updated Lifecycle Pet",
            photoUrls=new_pet.photoUrls,
            status="sold"
        )
        update_response = api_client.update_pet(updated_pet)
        assert_status_code(update_response, 200)
        
        verify_response = api_client.get_pet_by_id(pet_id)
        updated = assert_response_schema(verify_response, Pet)
        assert updated.name == "Updated Lifecycle Pet"
        assert updated.status == "sold"
        
        delete_response = api_client.delete_pet(pet_id)
        assert_status_code(delete_response, 200)
        
        final_response = api_client.get_pet_by_id(pet_id)
        assert_status_code(final_response, 404)
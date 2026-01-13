from typing import List, Optional
import requests
from api_tests.api.base_client import BaseAPIClient
from api_tests.models.pet import Pet

    
class PetClient(BaseAPIClient):
    
    def add_pet(self, pet: Pet) -> requests.Response:
        return self.post("pet", json_data=pet.model_dump(exclude_none=True))
    
    def update_pet(self, pet: Pet) -> requests.Response:
        return self.put("pet", json_data=pet.model_dump(exclude_none=True))
    
    def find_pets_by_status(self, status: List[str]) -> requests.Response:
        params = {"status": status}
        return self.get("pet/findByStatus", params=params)
    
    def find_pets_by_tags(self, tags: List[str]) -> requests.Response:
        params = {"tags": tags}
        return self.get("pet/findByTags", params=params)
    
    def get_pet_by_id(self, pet_id: int) -> requests.Response:
        return self.get(f"pet/{pet_id}")
    
    def update_pet_with_form(
        self,
        pet_id: int,
        name: Optional[str] = None,
        status: Optional[str] = None
    ) -> requests.Response:
        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.post(f"pet/{pet_id}", data=data, headers=headers)
    
    def delete_pet(self, pet_id: int) -> requests.Response:
        return self.delete(f"pet/{pet_id}")
    
    def upload_image(
        self,
        pet_id: int,
        file_path: str,
        additional_metadata: Optional[str] = None
    ) -> requests.Response:
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        filename = file_path.split("/")[-1]
        files = {"file": (filename, file_data, "image/png")}
        data = {}
        
        if additional_metadata:
            data["additionalMetadata"] = additional_metadata
        
        headers = {"Content-Type": None}
        
        return self.post(
            f"pet/{pet_id}/uploadImage",
            files=files,
            data=data if data else None,
            headers=headers
        )
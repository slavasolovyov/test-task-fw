import logging
from typing import Dict, Optional, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api_tests.config.settings import settings

logger = logging.getLogger(__name__)


class BaseAPIClient:

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or settings.get_base_url()
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        return session
    
    def _build_url(self, endpoint: str) -> str:
        
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url.rstrip('/')}/{endpoint}"
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        url = self._build_url(endpoint)
    
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        logger.info(f"Making {method} request to {url}")
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                data=data,
                files=files,
                headers=request_headers,
                timeout=settings.TIMEOUT,
                verify=settings.VERIFY_SSL,
                **kwargs
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text[:500]}")
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self._make_request("GET", endpoint, params=params, **kwargs)
    
    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        return self._make_request("POST", endpoint, json_data=json_data, data=data, files=files, **kwargs)
    
    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        return self._make_request("PUT", endpoint, json_data=json_data, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request("DELETE", endpoint, **kwargs)
    
    def close(self):
        self.session.close()

## client.py             Sends HTTP requests to the API server

# __init__  → remembers where the server is

# _request  → goes to the server, asks, and comes back with the answer

# get       → asks for data

# post      → sends data

# Defines the API Client class for communicating with the FastAPI server.
    # Defines a function called __init__ that receives an optional base URL.
        # Sets the base URL used by the client.
    # Defines a function called _request that receives an HTTP method, an endpoint, and optional request arguments.
        # Builds the complete API URL.
        # Sends the HTTP request to the API server.
        # Returns the JSON response.
        # Handles connection errors.
        # Handles timeout errors.
        # Handles HTTP errors.
        # Handles other request errors.
    # Defines a function called get that receives an endpoint and optional query parameters.
        # Sends a GET request to the API.
    # Defines a function called post that receives an endpoint and optional data.
        # Sends a POST request with JSON data.


import requests
from src.config import API_BASE_URL


# Defines the API Client class for communicating with the FastAPI server.
class APIClient:

    # Defines a function called __init__ that receives an optional base URL.
    def __init__(self, base_url: str = None):

        # Sets the provided base URL or the default API base URL.
        self.base_url = base_url or API_BASE_URL

    # Defines a function called _request that receives an HTTP method, an endpoint, and optional request arguments.
    def _request(self, method: str, endpoint: str, **kwargs):

        # Builds the complete API URL.
        url = f"{self.base_url}{endpoint}"

        try:
            # Sends the HTTP request to the API server.
            response = requests.request(
                method=method,
                url=url,
                timeout=5,          # Prevents the agent from getting stuck.
                **kwargs
            )

            # Checks if the API response contains an HTTP error.
            response.raise_for_status()

            # Returns the JSON response.
            return response.json()

        # Handles connection errors when the API server cannot be reached.
        except requests.exceptions.ConnectionError:
            return {"error": f"Could not connect to the server at {self.base_url}"}

        # Handles timeout errors when the API request takes too long.
        except requests.exceptions.Timeout:
            return {"error": "The API request timed out."}

        # Handles HTTP errors returned by the API server.
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}

        # Handles other request errors.
        except requests.exceptions.RequestException as e:
            return {"error": f"Unexpected request error: {str(e)}"}

    # Defines a function called get that receives an endpoint and optional query parameters.
    def get(self, endpoint: str, params: dict = None):

        # Sends a GET request to the API.
        return self._request("get", endpoint, params=params)

    # Defines a function called post that receives an endpoint and optional data.
    def post(self, endpoint: str, data: dict = None):

        # Sends a POST request with JSON data.
        return self._request("post", endpoint, json=data)


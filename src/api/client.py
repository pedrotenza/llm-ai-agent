# src/api/client.py
import requests
from src.config import API_BASE_URL


class APIClient:
    """Cliente HTTP genérico para comunicarse con la API FastAPI."""

    def __init__(self, base_url: str = None):
        """
        Inicializa el cliente.

        Args:
            base_url (str, optional): URL base de la API. Si no se proporciona,
                                      se usa el valor de API_BASE_URL desde config.
        """
        self.base_url = base_url or API_BASE_URL

    def _request(self, method: str, endpoint: str, **kwargs):
        """
        Método interno que ejecuta la petición HTTP y captura errores.

        Args:
            method (str): Método HTTP ('get' o 'post').
            endpoint (str): Ruta del endpoint (ej. "/machines").
            **kwargs: Argumentos adicionales para requests (params, json, etc.)

        Returns:
            dict: Respuesta JSON o dict con clave "error".
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=5,          # Evita que el agente se quede colgado
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": f"No se pudo conectar al servidor en {self.base_url}"}
        except requests.exceptions.Timeout:
            return {"error": "La solicitud a la API ha expirado (timeout)"}
        except requests.exceptions.HTTPError as e:
            return {"error": f"Error HTTP {e.response.status_code}: {e.response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error inesperado en la petición: {str(e)}"}

    def get(self, endpoint: str, params: dict = None):
        """
        Envía una petición GET.

        Args:
            endpoint (str): Ruta del endpoint.
            params (dict, optional): Parámetros de consulta.

        Returns:
            dict: Respuesta JSON o dict con "error".
        """
        return self._request("get", endpoint, params=params)

    def post(self, endpoint: str, data: dict = None):
        """
        Envía una petición POST con datos JSON.

        Args:
            endpoint (str): Ruta del endpoint.
            data (dict, optional): Datos a enviar en el cuerpo (se serializan a JSON).

        Returns:
            dict: Respuesta JSON o dict con "error".
        """
        return self._request("post", endpoint, json=data)
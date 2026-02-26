import pytest


@pytest.mark.integration
class TestHealthz:
    def test_status_code(self, integration_client):
        response = integration_client.get("/healthz")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    def test_response_body(self, integration_client):
        response = integration_client.get("/healthz")
        assert response.json() == {"status": "ok"}, f"Unexpected response content: {response.text}"

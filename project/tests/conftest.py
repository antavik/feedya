import pytest
import requests


@pytest.fixture
def http_response(request, mocker):
    status_code, text = request.param
    mock_response = mocker.Mock()

    if status_code in (400, 401, 402, 403, 404,):
        mock_response.status_code = status_code
        mock_response.raise_for_status.side_effect = requests.HTTPError
    else:
        mock_response.status_code = status_code
        mock_response.text = text

    return mock_response

"""Tests for OAuth authorization code exchange."""
from unittest.mock import patch, Mock
from auth import exchange_code_for_tokens


def test_exchange_code_for_tokens_returns_token_data():
    """Exchanges authorization code for access and refresh tokens."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'access_token': 'new_access_token_123',
        'refresh_token': 'new_refresh_token_456',
        'expires_at': 1234567890
    }

    with patch('requests.post', return_value=mock_response) as mock_post:
        result = exchange_code_for_tokens(
            client_id='test_client_id',
            client_secret='test_secret',
            code='auth_code_789'
        )

    assert result['access_token'] == 'new_access_token_123'
    assert result['refresh_token'] == 'new_refresh_token_456'

    # Verify API was called correctly
    mock_post.assert_called_once_with(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': 'test_client_id',
            'client_secret': 'test_secret',
            'code': 'auth_code_789',
            'grant_type': 'authorization_code'
        }
    )

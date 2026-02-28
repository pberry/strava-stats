"""Tests for WordPress client."""
import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from wordpress import create_post, load_wp_credentials, _markdown_to_html


def test_posts_to_wordpress_with_correct_body():
    """POSTs to {wp_url}/wp-json/wp/v2/posts with correct body."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {'id': 42, 'link': 'https://blog.example.com/?p=42'}

    with patch('wordpress.requests.post', return_value=mock_response) as mock_post:
        result = create_post(
            wp_url='https://blog.example.com',
            username='pat',
            app_password='xxxx',
            title='Weekly Activities',
            content='# Report\n\nSome content',
        )

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == 'https://blog.example.com/wp-json/wp/v2/posts'
        assert call_args[1]['json']['title'] == 'Weekly Activities'
        assert call_args[1]['json']['status'] == 'publish'
        assert call_args[1]['auth'] == ('pat', 'xxxx')

    assert result == {'id': 42, 'link': 'https://blog.example.com/?p=42'}


def test_sends_content_as_html():
    """Sends content as HTML with simple markdown conversion."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {'id': 1, 'link': 'https://blog.example.com/?p=1'}

    with patch('wordpress.requests.post', return_value=mock_response) as mock_post:
        create_post(
            wp_url='https://blog.example.com',
            username='pat',
            app_password='xxxx',
            title='Test',
            content='# Heading\n\n**bold text**\n\nParagraph here.',
        )

        sent_content = mock_post.call_args[1]['json']['content']
        assert '<h1>' in sent_content
        assert '<strong>' in sent_content


def test_raises_on_auth_failure():
    """Raises RuntimeError on 401 (auth failure)."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = 'Unauthorized'

    with patch('wordpress.requests.post', return_value=mock_response):
        with pytest.raises(RuntimeError, match="WordPress authentication failed"):
            create_post(
                wp_url='https://blog.example.com',
                username='pat',
                app_password='wrong',
                title='Test',
                content='Content',
            )


def test_raises_on_http_error():
    """Raises RuntimeError on other HTTP errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = 'Internal Server Error'

    with patch('wordpress.requests.post', return_value=mock_response):
        with pytest.raises(RuntimeError, match="WordPress API error.*500"):
            create_post(
                wp_url='https://blog.example.com',
                username='pat',
                app_password='xxxx',
                title='Test',
                content='Content',
            )


def test_load_wp_credentials():
    """Reads WP_URL, WP_USERNAME, WP_APP_PASSWORD from .env."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("WP_URL=https://blog.example.com\n")
        f.write("WP_USERNAME=pat\n")
        f.write("WP_APP_PASSWORD=xxxx xxxx xxxx\n")
        env_path = f.name

    try:
        env_clean = {k: v for k, v in os.environ.items() if not k.startswith('WP_')}
        with patch.dict(os.environ, env_clean, clear=True):
            creds = load_wp_credentials(env_file=env_path)

        assert creds == {
            'wp_url': 'https://blog.example.com',
            'username': 'pat',
            'app_password': 'xxxx xxxx xxxx',
        }
    finally:
        os.unlink(env_path)


def test_raises_when_wp_credential_missing():
    """Raises RuntimeError when any WP credential missing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("WP_URL=https://blog.example.com\n")
        env_path = f.name

    try:
        env_clean = {k: v for k, v in os.environ.items() if not k.startswith('WP_')}
        with patch.dict(os.environ, env_clean, clear=True):
            with pytest.raises(RuntimeError, match="WP_USERNAME not found"):
                load_wp_credentials(env_file=env_path)
    finally:
        os.unlink(env_path)


def test_markdown_to_html_converts_headings_and_bold():
    """Converts markdown headings and bold to HTML."""
    md = "# Title\n\n## Subtitle\n\n### Section\n\n**bold text**\n\nPlain paragraph."
    html = _markdown_to_html(md)

    assert "<h1>Title</h1>" in html
    assert "<h2>Subtitle</h2>" in html
    assert "<h3>Section</h3>" in html
    assert "<strong>bold text</strong>" in html
    assert "<p>Plain paragraph.</p>" in html


def test_markdown_to_html_converts_list_items():
    """Converts markdown list items to HTML list."""
    md = "- Item one\n- Item two\n- Item three"
    html = _markdown_to_html(md)

    assert "<li>" in html
    assert "Item one" in html

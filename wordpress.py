"""WordPress client for posting via REST API."""
import os
import re
import requests
from dotenv import load_dotenv


def create_post(wp_url, username, app_password, title, content):
    """Create a published post on WordPress."""
    html_content = _markdown_to_html(content)

    response = requests.post(
        f"{wp_url}/wp-json/wp/v2/posts",
        auth=(username, app_password),
        json={
            'title': title,
            'content': html_content,
            'status': 'publish',
        },
    )

    if response.status_code == 401:
        raise RuntimeError(
            f"WordPress authentication failed. Response: {response.text}"
        )

    if response.status_code != 201:
        raise RuntimeError(
            f"WordPress API error with status {response.status_code}. "
            f"Response: {response.text}"
        )

    data = response.json()
    return {'id': data['id'], 'link': data['link']}


def load_wp_credentials(env_file='.env'):
    """Load WordPress credentials from .env file."""
    load_dotenv(env_file, override=True)

    wp_url = os.getenv('WP_URL')
    username = os.getenv('WP_USERNAME')
    app_password = os.getenv('WP_APP_PASSWORD')

    if not wp_url:
        raise RuntimeError(f"WP_URL not found in {env_file}")
    if not username:
        raise RuntimeError(f"WP_USERNAME not found in {env_file}")
    if not app_password:
        raise RuntimeError(f"WP_APP_PASSWORD not found in {env_file}")

    return {
        'wp_url': wp_url,
        'username': username,
        'app_password': app_password,
    }


def _markdown_to_html(markdown):
    """Convert simple markdown subset to HTML."""
    lines = markdown.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        if line.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line[2:])
            html_lines.append(f"<li>{item}</li>")
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            converted = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            html_lines.append(f"<p>{converted}</p>")

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)

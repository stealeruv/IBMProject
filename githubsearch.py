import requests

def is_hex_64(s):
    try:
        int(s, 16)
        return len(s) == 64
    except ValueError:
        return False

def github_search_hex_string():
    base_url = "https://api.github.com/search/code"
    query = "filename:*.md extension:md "  # Adjust the query as needed
    query += "NOT repo:.github"  # Exclude certain repositories if needed

    params = {
        'q': query,
        'per_page': 10,  # Adjust the number of results per page as needed
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        results = response.json().get('items', [])
        for result in results:
            file_content_url = result['url']
            file_content_response = requests.get(file_content_url)
            if file_content_response.status_code == 200:
                file_content = file_content_response.json().get('content', '')
                if is_hex_64(file_content):
                    repository = result['repository']['full_name']
                    file_path = result['path']
                    print(f"Repository: {repository}, File Path: {file_path}")
            else:
                print(f"Error getting file content: {file_content_response.status_code}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Example usage:
github_search_hex_string()
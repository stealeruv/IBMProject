import requests
import time

def is_hex_64(s):
    try:
        int(s, 16)
        return len(s) == 64
    except ValueError:
        return False

def github_search_hex_string(access_token, search_query):
    base_url = "https://api.github.com/search/code"
    headers = {'Authorization': f'token {access_token}'}
    params = {
        'q': search_query,
        'per_page': 100,  # Adjust the number of results per page as needed
    }

    while True:
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json().get('items', [])
            for result in results:
                file_content_url = result['url']
                file_content_response = requests.get(file_content_url, headers=headers)
                if file_content_response.status_code == 200:
                    file_content = file_content_response.json().get('content', '')
                    if is_hex_64(file_content):
                        repository = result['repository']['full_name']
                        file_path = result['path']
                        print(f"Repository: {repository}, File Path: {file_path}")
            if 'next' in response.links:
                params['page'] = int(response.links['next']['url'].split('page=')[1])
            else:
                break
        elif response.status_code == 403:
            reset_time = int(response.headers['X-RateLimit-Reset'])
            sleep_time = max(0, reset_time - time.time()) + 1
            print(f"Rate limit exceeded. Waiting for {sleep_time} seconds.")
            time.sleep(sleep_time)
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break

# Example usage:
your_access_token = "YOUR_ACCESS_TOKEN"
search_query = "filename:*.md extension:md NOT repo:.github"  # Adjust the query as needed
github_search_hex_string(your_access_token, search_query)
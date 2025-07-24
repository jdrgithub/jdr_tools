import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Choose a target URL
url = "https://books.toscrape.com"

def fetch_url(url, method='GET', session=None, **kwargs):
    """Function to make web requests and handle errors."""
    try:
        if session:
            request_func = session.get if method == 'GET' else session.post
        else:
            request_func = requests.get if method == 'GET' else requests.post

        response = request_func(url, **kwargs)
        response.raise_for_status()
        logging.info(f"Request to {url} succeeded.")
        return response
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
    except requests.exceptions.Timeout:
        logging.error("The request timed out.")
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error occurred: {err}")
    return None

# Direct request without session
response = fetch_url(url, timeout=5)

# Using a session
with requests.Session() as session:
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    session_response = fetch_url(url, session=session, timeout=5)

# Handle authentication (optional test)
auth_url = "https://httpbin.org/basic-auth/user/passwd"
auth_response = fetch_url(auth_url, auth=('user', 'passwd'), timeout=5)

# Stream Downloads
stream_response = fetch_url("https://books.toscrape.com/static/images/banner.jpg", stream=True)
if stream_response:
    with open("banner.jpg", 'wb') as f:
        for chunk in stream_response.iter_content(chunk_size=8192):
            f.write(chunk)

# GET with query params
params = {'category': 'fiction', 'sort': 'price'}
response_with_params = fetch_url("https://books.toscrape.com/catalogue/category/books/fiction_10/index.html", params=params)

# Custom headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
response_headers = fetch_url("https://books.toscrape.com/", headers=headers)

# POST example
post_data = {"username": "test", "password": "1234"}
post_response = fetch_url("https://httpbin.org/post", method='POST', data=post_data)

# HEAD request for checking headers
head_response = fetch_url("https://books.toscrape.com/", method='HEAD')

# Handling redirects
redirect_response = fetch_url("http://books.toscrape.com")
non_redirect_response = fetch_url("http://books.toscrape.com", allow_redirects=False)

# Always use a browser-like User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Step 1: Download the page
response = requests.get(url, headers=headers)

# Step 2: Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Ensure response and soup are correctly initialized
response = fetch_url("https://books.toscrape.com")
if response:
    soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find all book titles (they're inside <h3> tags with <a> inside them)
for h3 in soup.find_all('h3'):
        a_tag = h3.find('a') # type: ignore
        if a_tag and 'title' in a_tag.attrs: # type: ignore
            title = a_tag['title']  # type: ignore # The book title is stored in the 'title' attribute
            print(title)
        else:
            logging.warning("No title found in h3 element.")
    

# Always use a browser-like User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Step 1: Download the page
response = requests.get(url, headers=headers)

# Step 2: Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find all book titles (they're inside <h3> tags with <a> inside them)
for h3 in soup.find_all('h3'):
    title = h3.find('a')['title']  # The book title is stored in the 'title' attribute
    print(title)





 


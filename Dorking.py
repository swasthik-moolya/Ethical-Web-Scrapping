import requests
from bs4 import BeautifulSoup
import time


def google_dork(query, num_results):
    """
    Performs a Google search using a dork query and fetches results.

    :param query: The Google Dork query.
    :param num_results: Number of results to retrieve.
    :return: List of search result URLs.
    """
    # Base URL for Google search
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    result_urls = []
    start = 0

    while len(result_urls) < num_results:
        params = {"q": query, "start": start}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch results: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all("a", href=True)

        for result in search_results:
            link = result['href']
            if "/url?q=" in link and not "webcache" in link:
                clean_link = link.split("/url?q=")[1].split("&")[0]
                result_urls.append(clean_link)
                if len(result_urls) >= num_results:
                    break

        start += 10
        time.sleep(1)  # To avoid triggering CAPTCHA

    return result_urls


def main():
    print("Welcome to Ethical Google Dorking Tool")
    print("Use this tool only for authorized and ethical purposes.")

    dork_query = input("Enter your Google Dork query: ")
    num_results = int(input("Enter the number of results to fetch: "))

    print(f"Performing Google Dorking with query: {dork_query}")
    results = google_dork(dork_query, num_results=num_results)

    if results:
        print("\nFound URLs:")
        for url in results:
            print(url)
    else:
        print("No results found or search was blocked.")


if __name__ == "__main__":
    main()

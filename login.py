import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the elements with a specific class or tag containing the article titles
        # Adjust this according to the structure of the website you're scraping
        article_titles = soup.find_all('h2', class_='article-title')  # Example: <h2 class="article-title">...</h2>
        
        # Extract and print the titles
        for title in article_titles:
            print(title.text.strip())  # .strip() removes leading/trailing whitespaces
    else:
        print("Failed to retrieve the webpage.")

# URL of the website to scrape
website_url = ''

# Call the function with the URL
scrape_website(website_url)

import requests
from bs4 import BeautifulSoup

def scrape_links():
    response = requests.get('https://www.food.com/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return [a.get('href') for div in soup.find_all('div', class_='body svelte-n9bgqc') for a in div.find_all('a') if a.get('href')]
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

def scrape_food(links):
    all_data = []
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        recipe = {
            'link': link,
            'image': extract_image(soup),
            'name': extract_name(soup),
            'ingredients': extract_ingredients(soup),
            'directions': extract_directions(soup)
        }

        all_data.append(recipe)

    return all_data

def extract_name(soup):
    name = soup.find('h1', class_='svelte-1muv3s8')
    return name.get_text(strip=True) if name else "Name not found"

def extract_image(soup):
    image_div = soup.find('div', class_='primary-image svelte-wgcq7z')
    if image_div:
        image = image_div.find('img')
        return image['src'] if image and 'src' in image.attrs else "Image not found"
    return "Image div not found"

def extract_ingredients(soup):
    ingredients_list = soup.find('ul', class_='ingredient-list svelte-1r658j4')
    return [li.get_text(strip=True) for li in ingredients_list.find_all('li')] if ingredients_list else []

def extract_directions(soup):
    directions_list = soup.find('ul', class_='direction-list svelte-1r658j4')
    return [li.get_text(strip=True) for li in directions_list.find_all('li')] if directions_list else []
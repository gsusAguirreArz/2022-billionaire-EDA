import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


def scrapper( page_source: str , sleep_time: int=1, verbose: bool=True ) -> list:
    soup = BeautifulSoup(page_source, 'lxml')

    if verbose:
        print("Scrapping page....")

    ranks = [ e.text for e in soup.findAll('div', class_="rank")]
    names = [ e.text for e in soup.find_all('div', class_="personName")]
    networths = [ e.text for e in soup.find_all('div', class_="netWorth")]
    ages = [e.text for e in soup.find_all('div', class_="age")]
    countries = [ e.text for e in soup.find_all('div', class_="countryOfCitizenship")]
    sources = [ e.text for e in soup.find_all('div', class_="source")]
    industries = [ e.text for e in soup.find_all('div', class_="category")]

    time.sleep(sleep_time)
    return [ranks, names, networths, ages, countries, sources, industries]

def main( url: str, N_pages:int=2, sleep_time:int=5, filename: str="out.csv", save: bool=True ) -> pd.core.frame.DataFrame:
    data = {
        'rank': [],
        'name': [],
        'networth': [],
        'age': [],
        'country': [],
        'source': [],
        'industry': [],
    }

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(sleep_time)

    for _ in range(N_pages):
        ranks, names, networths,  ages, countries, sources, industries = scrapper(driver.page_source)
        data['rank'] = [*data['rank'], *ranks]
        data['name'] = [*data["name"], *names]
        data['networth'] = [*data["networth"], *networths]
        data['age'] = [*data["age"], *ages]
        data['country'] = [*data["country"], *countries]
        data['source'] = [*data["source"], *sources]
        data['industry'] = [*data["industry"], *industries]

        next_page_btn = driver.find_element_by_class_name('next-page')
        next_page_btn.click()
        time.sleep(sleep_time)
    
    driver.quit()

    df = pd.DataFrame(data)

    if save:
        df.to_csv(filename)
    
    return df


if __name__ == "__main__":
    URL = "https://www.forbes.com/billionaires/"
    filename = "2022_billionaires"
    n_pages = 13
    df = main(URL, n_pages, filename= f"./out/{filename}.csv")
    print("="*70)
    print("Finished scrapping ", n_pages + 1, " pages.")
    print("DataFrame with ", len(df), " rows, and ", len(df.columns), " columns.")
    print(df.info())
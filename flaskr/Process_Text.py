from pokemontcgsdk import RestClient, Card
from .APIKEY import API_KEY
import requests
import requests_cache
import re


requests_cache.install_cache('pokemon_cache', expire_after=3600)

RestClient.configure(API_KEY)

def main():
    extract_number_from_image("")
def extract_number_from_image(text):
    print(f"searching this text: {text}")
    match = re.search(r'\d{3}/\d{3}', text)
    if match:
        print("Extracted Number:", match.group())
        return match.group()
    else:
        print("No match found.")
    return match


def find_card(set_name, card_number):

    card = Card.where(q=f'set.name:{set_name}+number:{card_number}')
    return card.images

if __name__ == '__main__':
    main()
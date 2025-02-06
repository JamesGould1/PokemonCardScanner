from pokemontcgsdk import RestClient, Card
#from .APIKEY import API_KEY
import requests
import requests_cache
import re


requests_cache.install_cache('pokemon_cache', expire_after=3600)

RestClient.configure("b2963db2-0a48-48d2-a3f8-e2ad4f5d782a")

def main():
    find_card("Paldea","071/193")

def extract_number_from_image(text):
    print(f"searching the text")
    match = re.search(r'\d{3}/\d{3}', text)
    if match:
        print("Extracted Number:", match.group())
        return match.group()
    else:
        print("No match found.")
    return match

def extract_number_from_image_with_set(text):
    print(f"searching the text")
    match = re.search(r'\d{3}/', text)
    if match:
        print("Extracted Number:", match.group())
        return match.group()
    else:
        print("No match found.")
    return match

def find_card(set_name, card_number):
    if len(card_number) > 2:
        split_numbers = card_number.split("/")
        left_number = int(split_numbers[0])
        right_number = split_numbers[1]
    else:
        left_number = card_number.lstrip("0")

    if set_name == "":
        cards = Card.where(q=f'set.printedTotal:{right_number} number:{left_number}')
    else:
        cards = Card.where(q=f'set.name:\"{set_name}\" number:{left_number}')
    card = cards[0]
    price = card.tcgplayer.prices
    prices = []
    if price.normal is not None:
        prices.append(f"<p>Normal: {price.normal.market}</p>")
    if price.holofoil is not None:
        prices.append(f"<p>Holofoil: {price.holofoil.market}</p>")
    if price.reverseHolofoil is not None:
        prices.append(f"<p>Reverse Holofoil: {price.reverseHolofoil.market}</p>")
    s = "".join(prices)
    return f'''
    <!doctype html>
    <link rel="stylesheet" href = "style.css">
    <h1>{card.name}</h1>
    <img src={card.images.small}>
    <br>
    <h2>Prices:</h2>
    <span>{s}</span>
    '''
if __name__ == '__main__':
    main()
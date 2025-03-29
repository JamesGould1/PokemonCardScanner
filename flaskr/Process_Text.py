from pokemontcgsdk import RestClient, Card
from .APIKEY import API_KEY
import requests
import requests_cache
import re


requests_cache.install_cache('pokemon_cache', expire_after=3600)

RestClient.configure(API_KEY)

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
        left_number = int(card_number)

    if set_name == "":
        cards = Card.where(q=f'set.printedTotal:{right_number} number:{left_number}')
    else:
        cards = Card.where(q=f'set.name:\"{set_name}\" number:{left_number}')
    card = cards[0]
    price = card.tcgplayer.prices
    prices = []

    if price.normal is not None:
        prices.append(f"""
        <form action="/addCard" method="POST">
            <input type=hidden name="card_name" value="{card.name}">
            <input type=hidden name="set_name" value="{card.set.name}">
            <input type=hidden name="rarity" value="Normal">
            <p>Normal: {price.normal.market}</p>
            <button type="submit">Add to your collection</button>
        </form>""")
    if price.holofoil is not None:
        prices.append(f"""
        <form action="/addCard" method="POST">
            <input type=hidden name="card_name" value="{card.name}">
            <input type=hidden name="set_name" value="{card.set.name}">
            <input type=hidden name="rarity" value="Holofoil">
            <p>Holofoil: {price.holofoil.market}</p>
            <button type="submit">Add to your collection</button>
        </form>""")
    if price.reverseHolofoil is not None:
        prices.append(f"""
        <form action="/addCard" method="POST">
            <input type=hidden name="card_name" value="{card.name}">
            <input type=hidden name="set_name" value="{card.set.name}">
            <input type=hidden name="rarity" value="Reverse Holofoil">
            <p>Reverse Holofoil: {price.reverseHolofoil.market}</p>
            <button type="submit">Add to your collection</button>
        </form>""")

    s = "".join(prices)
    #add css?\zoom in effect
    return f'''
    <!doctype html>
    <link rel="stylesheet" href = "style.css">
    <h1>{card.name}</h1>
    <img src={card.images.small} id="cardImage">
    <br>
     <img src={card.set.images.logo} width=150 height=50>
     <br>
    <h2>Prices:</h2>
    <span>{s}</span>
    <script>
        let cardImage = document.getElementById('cardImage');
            cardImage.addEventListener('click', function() {{
            if (cardImage.src === "{card.images.small}") {{
                cardImage.src = "{card.images.large}";
            }} else {{
                cardImage.src = "{card.images.small}";
            }}
        }});
    </script>
    '''
if __name__ == '__main__':
    main()
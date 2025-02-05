from pokemontcgsdk import RestClient, Card
from .APIKEY import API_KEY


RestClient.configure(API_KEY)

card = Card.where(q='set.name:generations card.number:1')
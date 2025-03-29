from flask import flash, request, redirect, Blueprint, current_app, render_template
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flaskr import *


database = Blueprint('database', __name__)

@database.route("/cards")
def cards_list():
    cards = Cards.query.all()
    return render_template("cards.html", cards=cards)

@database.route("/addCard", methods=['POST'])
def add_card():
    card_name = request.form.get("card_name")
    set_name = request.form.get("set_name")
    card = Cards(
      cardName = card_name,
      setName = set_name,
    )
    db.session.add(card)
    db.session.commit()
    return redirect("http://127.0.0.1:5000/cards")
from flask import Blueprint, request, abort, make_response
from ..models.author import Author
from .route_utilities import validate_model, create_model
from ..models.book import Book
from ..db import db

author_bp = Blueprint("author_bp", __name__, url_prefix="/authors")

@author_bp.post("")
def create_author():
    request_body = request.get_json()
    try:
        new_author = Author.from_dict(request_body)
    except KeyError as err:
        response = {"message": f"Invalid request: missing {err.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_author)
    db.session.commit()

    response = new_author.to_dict()
    return response, 201

@author_bp.get("")
def get_all_authors():
    query = db.select(Author)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Author.name.ilike(f"%{name_param}%"))

    authors = db.session.scalars(query.order_by(Author.id))
    # Use list comprehension syntax to create the list `authors_response`
    authors_response = [author.to_dict() for author in authors]

    return authors_response

@author_bp.post("/<author_id>/cats")
def create_book_with_author_id(author_id):
    author = validate_model(author_id)

    request_body = request.get_json()
    request_body["author_id"] = author.id

    try:
        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()
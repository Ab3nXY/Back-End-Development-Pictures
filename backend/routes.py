from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    item = next((item for item in data if item["id"] == id), None)

    if item:
        return jsonify(item), 200

    return {"message": f"Item with ID {id} not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    request_data = request.json

    # Check if a picture with the same ID already exists
    existing_picture = next((pic for pic in data if pic['id'] == request_data['id']), None)

    if existing_picture:
        # If a picture with the same ID exists, return a 302 response
        return jsonify({"Message": f"picture with id {request_data['id']} already present"}), 302
    else:
        # Otherwise, create and add the new picture to the list
        new_picture = {
            "id": request_data['id'],
            "pic_url": request_data.get('pic_url'),
            "event_country": request_data.get('event_country'),
            "event_state": request_data.get('event_state'),
            "event_city": request_data.get('event_city'),
            "event_date": request_data.get('event_date')
        }

        data.append(new_picture)

        # Return the new picture details with a 201 response
        return jsonify(new_picture), 201
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Get the picture with the given ID
    picture = next((p for p in pictures if p['id'] == id), None)

    # Check if the picture exists
    if picture:
        # Update the picture data based on the request JSON
        picture.update(request.json)

        # Return the updated picture
        return jsonify(picture), 200
    else:
        # If picture not found, return a 404 response
        return {"message": f"Picture with ID {id} not found"}, 404
    

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Get the index of the picture with the given ID
    index = next((index for index, p in enumerate(data) if p['id'] == id), None)

    # Check if the picture exists
    if index is not None:
        # Remove the picture from the list
        deleted_picture = data.pop(index)

        # Return a success message
        return jsonify({"message": f"Picture with ID {id} deleted successfully"}), 204
    else:
        # If picture not found, return a 404 response
        return jsonify({"message": f"Picture with ID {id} not found"}), 404
    

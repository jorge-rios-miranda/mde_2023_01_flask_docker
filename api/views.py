from . import controller
from flask import Blueprint, request, make_response

bp = Blueprint('images', __name__, url_prefix='/')


@bp.post("/image")
def post_image():
	# parameter min_confidence
    min_confidence = int(request.args.get("min_confidence",80))

	# validation for parameter data
    if not request.is_json or "data" not in request.json:
        return make_response({"description": "You must include the image in base64 in field called data in body request"}, 400)
    
	# parameter data (imagen in base64)
    imgstr = request.json["data"]

	# call to logic for insert an image
    data = controller.post_image(min_confidence, imgstr)
    
    return data


@bp.get("/images")
def get_images():
	# parameter min_date
    min_date = request.args.get("min_date")
	# parameter max_date
    max_date = request.args.get("max_date")
	# parameter tags
    tags = request.args.get("tags") 
   
	# call to logic for list images
    data = controller.get_images(min_date, max_date, tags)
    
    return data


@bp.get("/image/<image_id>")
def get_image(image_id):
	if not image_id or not image_id.isnumeric():
		return make_response({"description": "Wrong image_id"}, 400)
    
	# call to logic for search an image
	data = controller.get_image(image_id)
    
	return data


@bp.get("/tags")
def get_tags():
	# parameter min_date
	min_date = request.args.get("min_date")	
	# parameter max_date
	max_date = request.args.get("max_date")

	# call to logic for list images
	data = controller.get_tags(min_date, max_date)
    
	return data



@bp.get("/test")
def test():
	return {"prueba01": 'Successful'}

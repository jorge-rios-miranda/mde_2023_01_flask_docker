from . import models
import io
import os
import uuid #For random filenames
import json
import base64
import requests
from imagekitio import ImageKit

images_path = '/images_api/'

with open('credentials.json', 'r') as credentials_file:
	credentials = json.load(credentials_file)

# controller function for register a new image
def post_image(min_confidence, imgstr):
	
	# Imagekit credentials
	imagekit = ImageKit(
		public_key= credentials['ImageKit']['public_key'],
		private_key= credentials['ImageKit']['private_key'],
		url_endpoint = credentials['ImageKit']['url_endpoint']
	)

	# Imagga credentials
	api_key = credentials['Imagga']['api_key']
	api_secret = credentials['Imagga']['api_secret']

	# upload an image
	upload_info = imagekit.upload(file=imgstr, file_name="my_file_name")
	
	# search tags
	response = requests.get(f"https://api.imagga.com/v2/tags?image_url={upload_info.url}", auth=(api_key, api_secret))

	# delete an uploaded image
	delete = imagekit.delete_file(file_id=upload_info.file_id)

	# random name for filename
	filename = str(uuid.uuid4())

	# decode and save image in local filesystem
	with open(images_path+filename, "wb") as image:	
		decoded_data=base64.b64decode((imgstr))		
		image.write(decoded_data)

	# insert image
	image_id = models.insert_image(images_path, filename, min_confidence, response.json()["result"]["tags"])
	
	# invoque get_image logic
	return get_image(image_id)
	

# controller function for list images
def get_images(min_date, max_date, tags):

	# search images in the database
	data =  models.get_images(min_date, max_date, tags)
	
	for d in data:
		d['size'] = round(os.path.getsize(d['path'])/1024)
		d['date'] = d['date'].strftime("%Y-%m-%d %H:%M:%S")
		d['tags'] = d['tags'].split(",")
		del d['path']

	return data

# controller function for list images
def get_image(image_id):
	
	result = {}
	
	# search an image in the database
	data = models.get_image(image_id)

	if len(data) == 0:
		return result
		
	else:
		# extract header image data
		result['id'] = data[0]['id']
		result['size'] = round(os.path.getsize(data[0]['path'])/1024)
		result['date'] = data[0]['date'].strftime("%Y-%m-%d %H:%M:%S")

		# read image file
		with open(data[0]['path'], "rb") as f:
			bstr = f.read()
			# encode image in base64
			result['data'] = base64.b64encode(bstr).decode()

		# search tags associate to the image
		data = models.get_tags_from_image(image_id)

		# return tags as list
		result['tags'] = data


	return result


# controller function for list tags
def get_tags(min_date, max_date):

	# search tags in the database
	data = models.get_tags(min_date, max_date)
	
	return data
 
	

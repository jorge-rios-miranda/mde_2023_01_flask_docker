from sqlalchemy import create_engine

# utility function to connect with database
def connect_db():
	engine = create_engine("mysql+pymysql://mbit:mbit@mysql_db/pictures")
	return engine.connect()


# utility function to convert SQL result to dict
def convert_db_result(result):
	return [
		dict(zip(result.keys(), row))
		for row in result
	]


# function to insert an image and tags
def insert_image(images_path, filename, min_confidence, tags):
	
	# connect to database
	with connect_db() as conn:
		# insert picture - default date is CURRENT_TIMESTAMP, then is inserted null
		result = conn.execute(f"INSERT INTO pictures (path) VALUES ('{images_path+filename}')")
		
		# recover last autoincremental id
		picture_id = result.lastrowid
		
		# insert tags
		for t in tags:
			# only when is great than min_confidence
			if t["confidence"] > min_confidence:
				conn.execute(f"INSERT INTO tags (tag,picture_id,confidence) VALUES ('{t['tag']['en']}',{picture_id},{t['confidence']})")
		
		return picture_id
	
	
# function to search images
def get_images(min_date, max_date, tags):

	# initial query
	query = """
		SELECT p.id, p.path, p.date, GROUP_CONCAT(t.tag) as tags 
						FROM pictures p 
						LEFT JOIN tags t ON p.id = t.picture_id
						WHERE 1 = 1
	"""
	
	# add filter for min_date
	if min_date:
		query += " AND p.date >= '{}'".format(min_date)

	# add filter for max_date
	if max_date:
		query += " AND p.date <= '{}'".format(max_date)

	# add filter for tags
	if tags:
		for tag in tags.split(","):
			query += " AND exists (select 1 from tags t2 where t2.picture_id = p.id and t2.tag = '{}')".format(tag)

	# final part of query
	query += " GROUP BY p.id, p.path, p.date"
	
	# connect and search
	with connect_db() as conn:
		result = conn.execute(query)

		return convert_db_result(result)

	
# function to search images
def get_image(image_id):
	
	# initial query
	query = """
		SELECT p.id, p.path, p.date 
		FROM pictures p 
		WHERE p.id = {}
	""".format(image_id)
	
	# connect and search
	with connect_db() as conn:
		result = conn.execute(query)
		
		return convert_db_result(result)
	
	
def get_tags_from_image(image_id):
	
	# initial query
	query = """
		SELECT t.tag, t.confidence 
		FROM tags t 
		WHERE t.picture_id = {}
	""".format(image_id)

	# connect and search
	with connect_db() as conn:
		result = conn.execute(query)

		return convert_db_result(result)
	

def get_tags(min_date, max_date):

	# initial query
	query = """
			SELECT t.tag, 
			count(t.picture_id) as n_images,
			min(confidence) as min_confidence,
			min(confidence) as max_confidence,
			avg(confidence) as mean_confidence
			FROM tags t 
			INNER JOIN pictures p ON p.id = t.picture_id
			where 1 = 1
	"""
	
	# add filter for min_date
	if min_date:
		query += " AND p.date >= '{}'".format(min_date)

	# add filter for max_date
	if max_date:
		query += " AND p.date <= '{}'".format(max_date)

	# final part of query
	query += " GROUP BY t.tag"
	
	# connect and search
	with connect_db() as conn:
		result = conn.execute(query)

		return convert_db_result(result)

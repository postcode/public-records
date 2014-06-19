### @export "Record"
class Record(db.Model):
# A record that is attached to a particular request. A record can be online (uploaded document, link) or offline.
	__tablename__ = 'record'
	id = db.Column(db.Integer, primary_key = True)
	date_created = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # The user who uploaded the record, right now only city staff can
	doc_id = db.Column(db.Integer) # The document ID. Currently using Scribd API to upload documents.
	request_id = db.Column(db.Integer, db.ForeignKey('request.id')) # The request this record was uploaded for
	description = db.Column(db.String(400)) # A short description of what the record is. 
	filename = db.Column(db.String(400)) # The original name of the file being uploaded.
	url = db.Column(db.String()) # Where it exists on the internet.
	download_url = db.Column(db.String()) # Where it can be downloaded on the internet.
	access = db.Column(db.String()) # How to access it. Probably only defined on offline docs for now.
	def __init__(self, request_id, user_id, url = None, filename = None, doc_id = None, description = None, access = None):
		self.doc_id = doc_id
		self.request_id = request_id
		self.user_id = user_id
		self.date_created = datetime.now().isoformat()
		self.description = description
		self.url = url
		self.filename = filename
		self.access = access
	def __repr__(self):
		return '<Record %r>' % self.description

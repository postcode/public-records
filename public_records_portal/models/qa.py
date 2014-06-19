### @export "QA"
class QA(db.Model):
# A Q & A block for a request
	__tablename__ = 'qa'
	id = db.Column(db.Integer, primary_key = True)
	question = db.Column(db.String())
	answer = db.Column(db.String())
	request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Actually just a user ID
	subscriber_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Actually just a user ID
	date_created = db.Column(db.DateTime)
	def __init__(self, request_id, question, owner_id = None):
		self.question = question
		self.request_id = request_id
		self.date_created = datetime.now().isoformat()
		self.owner_id = owner_id
	def __repr__(self):
		return "<QA Q: %r A: %r>" %(self.question, self.answer)

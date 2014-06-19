### @export "Subscriber"
class Subscriber(db.Model): 
# A person subscribed to a request, who may or may not have created the request, and may or may not own a part of the request.
	__tablename__ = 'subscriber'
	id = db.Column(db.Integer, primary_key = True)
	should_notify = db.Column(db.Boolean, default = True) # Allows a subscriber to unsubscribe
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = relationship("User", uselist = False)
	request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
	date_created = db.Column(db.DateTime)
	owner_id = db.Column(db.Integer, db.ForeignKey('owner.id')) # Not null if responsible for fulfilling a part of the request. UPDATE 6-11-2014: This isn't used. we should get rid of it.
 	def __init__(self, request_id, user_id, creator = False):
 		self.user_id = user_id
		self.request_id = request_id
		self.date_created = datetime.now().isoformat()
	def __repr__(self):
		return '<Subscriber %r>' %self.user_id

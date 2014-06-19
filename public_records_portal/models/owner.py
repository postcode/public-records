### @export "Owner"
class Owner(db.Model): 
# A member of city staff assigned to a particular request, that may or may not upload records towards that request.
	__tablename__ = 'owner'
	id = db.Column(db.Integer, primary_key =True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship("User", uselist = False)
	request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
	request = relationship("Request", foreign_keys = [request_id])
	active = db.Column(db.Boolean, default = True) # Indicate whether they're still involved in the request or not.
	reason = db.Column(db.String()) # Reason they were assigned
	reason_unassigned = db.Column(db.String()) # Reason they were unassigned
	date_created = db.Column(db.DateTime)
	date_updated = db.Column(db.DateTime)
	is_point_person = db.Column(db.Boolean)
	def __init__(self, request_id, user_id, reason= None, is_point_person = False):
		self.reason = reason
		self.user_id = user_id
		self.request_id = request_id
		self.date_created = datetime.now().isoformat()
		self.date_updated = self.date_created
		self.is_point_person = is_point_person
	def __repr__(self):
		return '<Owner %r>' %self.user_id

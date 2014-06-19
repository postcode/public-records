### @export "Department"
class Department(db.Model):
	__tablename__ = 'department'
	id = db.Column(db.Integer, primary_key =True)
	date_created = db.Column(db.DateTime)
	date_updated = db.Column(db.DateTime)
	name = db.Column(db.String(), unique=True)
	users = relationship("User") # The list of users in this department
	requests = relationship("Request", order_by = "Request.date_created.asc()") # The list of requests currently associated with this department
	def __init__(self, name):
		self.name = name
		self.date_created = datetime.now().isoformat()
	def __repr__(self):
		return '<Department %r>' % self.name
	def __str__(self):
		return self.name
	def get_name(self):
		return self.name or "N/A"

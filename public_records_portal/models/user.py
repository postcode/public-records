### @export "User"
class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	alias = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	phone = db.Column(db.String())
	date_created = db.Column(db.DateTime)
	password = db.Column(db.String(255))
	department = db.Column(Integer, ForeignKey("department.id"))
	current_department = relationship("Department", foreign_keys = [department], uselist = False)
	contact_for = db.Column(db.String()) # comma separated list
	backup_for = db.Column(db.String()) # comma separated list
	owners = relationship("Owner")
	subscribers = relationship("Subscriber")

	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return unicode(self.id)
	def set_password(self, password):
		self.password = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password, password)
	def get_alias(self):
		if self.alias and self.alias != "":
			return self.alias
		return "N/A"
	def get_phone(self):
		if self.phone and self.phone != "":
			return self.phone
		return "N/A"
	def __init__(self, email=None, alias = None, phone=None, department = None, password=None):
		self.email = email
		self.alias = alias
		if phone != "":
			self.phone = phone
		self.date_created = datetime.now().isoformat()
		if password:
			self.set_password(password)
		else:
			self.set_password(app.config['ADMIN_PASSWORD'])
		self.department = department
	def __repr__(self):
		return '<User %r>' % self.email
	def __str__(self):
		return self.email
	def department_name(self):
		if self.current_department and self.current_department.name:
			return self.current_department.name
		else:
			app.logger.error("\n\nUser %s is not associated with a department." % self.email)
			return "N/A"

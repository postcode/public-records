### @export "Request"
class Request(db.Model): 
# The public records request
	__tablename__ = 'request'
	id = db.Column(db.Integer, primary_key =True)
	date_created = db.Column(db.DateTime)
	due_date = db.Column(db.DateTime)
	extended = db.Column(db.Boolean, default = False) # Has the due date been extended?
	qas = relationship("QA", cascade="all,delete", order_by = "QA.date_created.desc()") # The list of QA units for this request
	status_updated = db.Column(db.DateTime)
	text = db.Column(db.String(), unique=True) # The actual request text.
	owners = relationship("Owner", cascade = "all, delete", order_by="Owner.date_created.asc()")
	subscribers = relationship("Subscriber", cascade ="all, delete") # The list of subscribers following this request.
	current_owner = db.Column(Integer) # Deprecated
	records = relationship("Record", cascade="all,delete", order_by = "Record.date_created.desc()") # The list of records that have been uploaded for this request.
	notes = relationship("Note", cascade="all,delete", order_by = "Note.date_created.desc()") # The list of notes appended to this request.
	status = db.Column(db.String(400)) # The status of the request (open, closed, etc.)
	creator_id = db.Column(db.Integer, db.ForeignKey('user.id')) # If city staff created it on behalf of the public, otherwise the creator is the subscriber with creator = true
	department = db.Column(db.String())
	department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
	department_obj = relationship("Department", uselist = False)
	date_received = db.Column(db.DateTime)
	offline_submission_type = db.Column(db.String())

	def __init__(self, text, creator_id = None, department = None, offline_submission_type = None, date_received = None):
		self.text = text
		self.date_created = datetime.now().isoformat()
		self.creator_id = creator_id
		self.department = department
		self.offline_submission_type = offline_submission_type
		if date_received and type(date_received) is datetime:
				self.date_received = date_received

	def __repr__(self):
		return '<Request %r>' % self.text

	def set_due_date(self):
		date_received = self.date_received
		if not date_received:
			date_received = self.date_created
		if self.extended == True:
			self.due_date = date_received + timedelta(days = int(app.config['DAYS_AFTER_EXTENSION']))
		else:
			self.due_date = date_received + timedelta(days = int(app.config['DAYS_TO_FULFILL']))

	def extension(self):
		self.extended = True 
		self.due_date = self.due_date + timedelta(days = int(app.config['DAYS_AFTER_EXTENSION']))
	def point_person(self):
		for o in self.owners:
			if o.is_point_person:
				return o
		return None
	def all_owners(self):
		all_owners = []
		for o in self.owners:
			all_owners.append(o.user.get_alias())
		return all_owners
		
	def requester(self):
		if self.subscribers:
			return self.subscribers[0] or None # The first subscriber is always the requester
		return None

	def requester_name(self):
		requester = self.requester()
		if requester and requester.user:
			return requester.user.get_alias()
		return "N/A"

	def requester_phone(self):
		requester = self.requester()
		if requester and requester.user:
			return requester.user.get_phone()
		return "N/A"
	def point_person_name(self):
		point_person = self.point_person()
		if point_person and point_person.user:
			return point_person.user.get_alias()
		return "N/A"
	def department_name(self):
		if self.department_obj:
			return self.department_obj.get_name()
		return "N/A"
	def is_closed(self):
		if self.status:
			return re.match('.*(closed).*', self.status, re.IGNORECASE) is not None
		else:
			app.logger.info("\n\n Request with this ID has no status: %s" % self.id)
			return False
	def solid_status(self, cron_job = False):
		if self.is_closed():
			return "closed"
		else:
			if cron_job or (not current_user.is_anonymous()):
				if self.due_date:
					if datetime.now() >= self.due_date:
						return "overdue"
					elif (datetime.now() + timedelta(days = 2)) >= self.due_date:
						return "due soon"
		return "open"

### @export "Visualization"
class Visualization(db.Model):
	__tablename__ = 'visualization'
	id = db.Column(db.Integer, primary_key = True)
	content = db.Column(db.String())
	date_created = db.Column(db.DateTime)
	date_updated = db.Column(db.DateTime)
	type_viz = db.Column(db.String())
	def __init__(self, type_viz, content):
		self.type_viz = type_viz
		self.content = content
		self.date_created = datetime.now().isoformat()
	def __repr__(self):
		return '<Visualization %r>' % self.type_viz

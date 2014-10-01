from public_records_portal import models, db
import csv

def export():
	records = models.Request.query.order_by(models.Request.id).all()
	db_headers = ['id', 'text', 'date_received', 'date_created', 'due_date', 'extended']
	all_headers = ['Request ID', 'Request Text', 'Date Received', 'Date Created', 'Date Due', 'Extended?', 'Requester Name', 'Requester Phone', 'Department Name', 'Point of Contact', 'All staff involved', 'Status']
	yield ','.join(all_headers) + '\n'
	for curr in records:
		row = []
		for name in db_headers:
			if name == 'text':
				text = getattr(curr,'text')
				text = text.replace('\n', '').replace('\r', '').replace('\t', '').replace('"', '\'')
				text = text.encode('utf8')
				row.append('"%s"' % str(text))
				continue
			row.append(str(getattr(curr,name)))
		row.append('"%s"' % str(curr.requester_name().encode('utf8')))
		row.append('"%s"' % str(curr.requester_phone()))
		row.append('"%s"' % str(curr.department_name()))
		row.append('"%s"' % str(curr.point_person_name()))
		row.append('"%s"' % str(','.join(curr.all_owners())))
		row.append('"%s"' % str(curr.solid_status(cron_job = True)))
		yield ','.join(row) + '\n'
		print row

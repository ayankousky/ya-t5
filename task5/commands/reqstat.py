from .base import Base
import csv
import operator


class ReqStat(Base):

	def run(self):
		users = {}
		csv_path = self.options['-f']
		empty = self.options['--empty']
		with open(csv_path, 'rb') as csvfile:
			journal = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in journal:
				if row[1] == '""src_user""':
					continue
				if not empty and row[1] is '':
					continue
				if users.get(row[1]):
					users[row[1]] += 1
				else:
					users[row[1]] = 1
			top_req_users = sorted(users.items(), key=operator.itemgetter(1), reverse=True)
			for user in top_req_users[0:5]:
				print 'src_user "' + user[0] + '" made ' + str(users.get(user[0])) + ' requests'

"""The hello command."""

from json import dumps

from .base import Base
import csv
import operator


class Users: pass


class ReqStat(Base):
	"""Say hello, world!"""

	def run(self):
		users = {}# Users();
		# with open('/Users/alex/Desktop/short.csv', 'rb') as csvfile:
		with open('/Users/alex/Desktop/shkib.csv', 'rb') as csvfile:
			journal = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in journal:
				if row[1] == '""src_user""':
					continue
				if users.get(row[1]):
					users[row[1]] += 1
				else:
					users[row[1]] = 1
			top_req_users = sorted(users.items(), key=operator.itemgetter(1), reverse=True)
			for user in top_req_users[0:6]:
				print user[0] +' '+str(users.get(user[0]))

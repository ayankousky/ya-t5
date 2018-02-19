from .base import Base
import csv
import time
from datetime import datetime
import re
import hashlib


class RegularByIp(Base):

	def run(self):
		dateStart = datetime.now()

		def getReqByHash(reqs, hash):
			return reqs.get(hash)

		def buildReqHash(timestamp, src_ip):
			return hashlib.sha1(str(int(timestamp)) + src_ip).hexdigest()

		duration = self.options['--duration'] or 120  # in minutes
		duration = int(duration)
		min_repeats = self.options['--min_repeats'] or 8  # count
		min_repeats = int(min_repeats)
		csv_path = self.options['-f']
		src_ip_filter = self.options['--src_ip'] or None
		period = self.options['--period'] or 1440
		period = int(period)
		empty = self.options['--empty']

		IPs = {}
		results = {}
		headLine = ''
		with open(csv_path, 'rb') as csvfile:
			journal = csv.reader(csvfile, delimiter=',', quotechar='|')
			headLine = next(csvfile)
			for row in journal:
				if not empty and row[2] is '':  # do not include requests without src_ip field
					continue
				if not re.match(r"^\"201.*0300\"$", row[0]):  # parse requests only with date
					continue
				if src_ip_filter is not None and src_ip_filter != row[2]:  # filter data if src_ip filter is set
					continue

				req_timestamp = int(time.mktime(datetime.strptime(row[0].replace('"', ''), '%Y-%m-%dT%H:%M:%S.%f+0300').timetuple()) / 60 )
				hash = buildReqHash(req_timestamp, row[2]) # !Important: use hash instead of just timestamp so we can extend selector at any time. F.i. we can add "input_byte" filed into hash (in case when it is requreid)
				row.append(req_timestamp)  # remember timestamp for the next uses
				if IPs.get(row[2]) is None:
					IPs[row[2]] = {}
				IPs[row[2]][hash] = row

			for ip in IPs.keys():
				ip_dict = IPs.get(ip)
				ip_results = []
				for step in range(1, period):

					min_seq = duration / step  # a minimum occurrence threshold during specified duration
					if min_seq < min_repeats:
						break

					for hash in ip_dict.keys():
						interval = step
						curr_req = ip_dict.get(hash)
						regular_reqs = [curr_req]
						for x in range(0, min_seq):
							next_req = getReqByHash(ip_dict, buildReqHash(curr_req[9] + interval, ip))  # build hash for the next value in sequence
							if next_req is None:  # if next value is not found - this is not a periodical requests
								regular_reqs = None
								break
							interval += step  # prepare to find next value
							regular_reqs.append(next_req)
						if regular_reqs is not None:
							ip_results.append(regular_reqs)
				if len(ip_results) is not 0:
					print 'Found for ' + ip + ' ' + str(len(ip_results)) + ' periodic requests'
				results[ip] = ip_results

		report_file = open('results.txt', 'w')
		for ip in results:
			if len(results.get(ip)) is 0:
				continue
			print >>report_file, "Src_ip: " + ip
			for reqs in results.get(ip):
				print >>report_file, '________________________________________________________'
				print >>report_file, 'Requests interval: ' + str(reqs[1][9] - reqs[0][9]) + ' minutes'
				print >>report_file, headLine.replace('\n', '')
				for r in reqs:
					print >>report_file, ','.join(r[:len(r)-1])




		print '________________________________________________________'
		print dateStart.strftime("%Y-%m-%d %H:%M:%S")
		endDate = datetime.now()
		print endDate.strftime("%Y-%m-%d %H:%M:%S")

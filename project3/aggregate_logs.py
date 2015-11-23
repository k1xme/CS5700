exp1_tcps = ["Newreno", "Reno", "Tahoe", "Vegas"]
exp2_tcps = ["Newreno_Reno", "Reno_Reno", "Newreno_Vegas", "Vegas_Vegas"]
exp3_tcps = ["Reno", "Sack1"]

# return: througput in kbps.
def calculate_benchmarks(fname):
	total_received_size = total_packets_sent = total_packets_received = 0
	window = {}
	sum_rtt = 0
	max_win = 0
	for line in open(fname):
		event, time, start, end, ptype, size, _, _, source, dest, seq, _ = line.split()

		if ptype == "tcp" and event == "-" and float(start) == float(source):
			total_packets_sent += 1
			window[seq] = float(time)
			max_win = max(max_win, len(window))
		if ptype == "ack" and event == "r" and float(end) == float(dest):
			total_packets_received += 1
			total_received_size += int(size)
			sum_rtt += float(time) - window[seq]
			window.pop(seq)

	rtt = sum_rtt / total_packets_received
	print total_packets_received, total_packets_sent, max_win*1040*8/rtt/1000000
	droprate = 1- float(total_packets_received)/total_packets_sent
	througput = (1040 * 8 / rtt) / 1000000

	return througput, droprate, rtt	

print calculate_benchmarks("exp1_trace/Reno_cbr_1.tr")
print calculate_benchmarks("project33.tr")

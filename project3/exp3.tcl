#Create a simulator object
set ns [new Simulator]

#Set color for flows
$ns color 1 Green
$ns color 2 Blue

#Read rate of cbr and variant of tcp from the command line
#Check availbility of inputs
if {$argc != 2} {
        puts "The script requires 2 arguments"
        puts "The first parameter is the type of the queue discpline"
        puts "The second parameter is the variant of the tcp"
        exit 1
}

#Open the trace file
set trace_name exp3_trace/
set tcp_variant [lindex [split [lindex $argv 1] /] 1]
append trace_name $tcp_variant
append trace_name _[lindex $argv 0].tr
set nf [open $trace_name w]
$ns trace-all $nf


#Define a 'finish' procedure
proc finish {} {
        global ns nf
        $ns flush-trace
        #Close the trace file
        close $nf
        exit 0
}

#Create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

if {[lindex argv 0] == "DropTail"} {
	$ns duplex-link $n1 $n2 10Mb 10ms DropTail
	$ns duplex-link $n2 $n5 10Mb 10ms DropTail
	$ns duplex-link $n2 $n3 10Mb 10ms DropTail
	$ns duplex-link $n3 $n4 10Mb 10ms DropTail
	$ns duplex-link $n3 $n6 10Mb 10ms DropTail
} else {
	$ns duplex-link $n1 $n2 10Mb 10ms RED
	$ns duplex-link $n2 $n5 10Mb 10ms RED
	$ns duplex-link $n2 $n3 10Mb 10ms RED
	$ns duplex-link $n3 $n4 10Mb 10ms RED
	$ns duplex-link $n3 $n6 10Mb 10ms RED
}
#Create links between the nodes using given queuing discpline


#Set CBR agent.
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp

#Create a Null agent (a traffic sink) and attach it to node n3
set null [new Agent/Null]
$ns attach-agent $n6 $null

set tcp [new Agent/[lindex $argv 1]]
$ns attach-agent $n1 $tcp

if {$tcp_variant != "Reno"} {
	set sink [new Agent/TCPSink/Sack1]	
} else {
	set sink [new Agent/TCPSink]
}
$ns attach-agent $n4 $sink

set ftp [new Application/FTP]
$ftp attach-agent $tcp

$ns connect $udp $null
$udp set fid_ 1
$ns connect $tcp $sink
$tcp set fid_ 2

$ns at 0.0 "$ftp start"
$ns at 3.0 "$cbr start"
$ns at 10.0 "$ftp stop"
$ns at 10.0 "$cbr stop"
$ns at 15.0 "finish"

$ns run
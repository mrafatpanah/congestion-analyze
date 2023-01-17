set ns [new Simulator]

$ns color 1 Blue
$ns color 2 Red

set namfile [open yeah.nam w]
$ns namtrace-all $namfile
set tracefile1 [open yeahTrace.tr w]
$ns trace-all $tracefile1


set wf1 [open WinFile1 w]
set wf2 [open WinFile2 w]

proc finish {} {
    global ns namfile
    $ns flush-trace
    #Close the NAM trace file
    close $namfile
    #Execute NAM on the trace file
    # exec xgraph WinFile1 -geometry 800x400 &
    # exec xgraph WinFile2 -geometry 800x400 &
    exec nam yeah.nam &
    exit 0
}

set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

$ns duplex-link $n1 $n3 4000Mb 500ms DropTail
$ns duplex-link $n2 $n3 4000Mb 800ms DropTail 
$ns duplex-link $n3 $n4 1000Mb 500ms DropTail
$ns duplex-link $n4 $n5 4000Mb 500ms DropTail
$ns duplex-link $n4 $n6 4000Mb 800ms DropTail
 #[expr {double(round(100*$rndVar2))/100}]


$ns queue-limit $n3 $n4 10
$ns queue-limit $n4 $n3 10

$ns duplex-link-op $n1 $n3 orient right-down
$ns duplex-link-op $n2 $n3 orient right-up
$ns duplex-link-op $n3 $n4 orient right
$ns duplex-link-op $n4 $n5 orient right-up
$ns duplex-link-op $n4 $n6 orient right-down


# $ns duplex-link-op $n3 $n4 queuePos 0.66
# $ns duplex-link-op $n4 $n3 queuePos 0.33
# Agent/TCP/Newreno

set source1 [new Agent/TCP/Linux]
$source1 set class_ 1
$source1 set ttl_ 64
$source1 set fid_ 1
$source1 set window_ 8000
$source1 set packetSize_ 10000
$ns attach-agent $n1 $source1
$ns at 0 "$source1 select_ca yeah"

set sink1 [new Agent/TCPSink/Sack1]
$sink1 set class_ 1
$sink1 set ts_echo_rfc1323_ true
$ns attach-agent $n5 $sink1

$ns connect $source1 $sink1



set source2 [new Agent/TCP/Linux]
$source2 set class_ 2
$source2 set ttl_ 64
$source2 set fid_ 2
$source2 set window_ 8000
$source2 set packetSize_ 1000
$ns attach-agent $n2 $source2
$ns at 0 "$source2 select_ca yeah"

set sink2 [new Agent/TCPSink]
$sink2 set class_ 2
$sink2 set ts_echo_rfc1323_ true
$ns attach-agent $n6 $sink2

$ns connect $source2 $sink2

$source1 attach $tracefile1
$source1 tracevar cwnd_
$source1 tracevar ssthresh_
$source1 tracevar ack_
$source1 tracevar maxseq_
$source1 tracevar rtt_

$source2 attach $tracefile1
$source2 tracevar cwnd_
$source2 tracevar ssthresh_
$source2 tracevar ack_
$source2 tracevar maxseq_
$source2 tracevar rtt_


set myftp1 [new Application/FTP]
$myftp1 attach-agent $source1


set myftp2 [new Application/FTP]
$myftp2 attach-agent $source2


$ns at 0.0 "$myftp2 start"
$ns at 0.0 "$myftp1 start"

proc plotWindow {tcpSource file} {
     global ns

     set time 1
     set now [$ns now]
     set cwnd [$tcpSource set cwnd_]
     set wnd [$tcpSource set window_]
     puts $file "$now $cwnd"
     $ns at [expr $now+$time] "plotWindow $tcpSource $file" 
  }
$ns at 0.1 "plotWindow $source1 $wf1"
$ns at 0.1 "plotWindow $source2 $wf2"

$ns at 1000.0 "finish"

puts "running..."

$ns run


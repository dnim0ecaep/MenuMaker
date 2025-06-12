complete -c bandwhich -s i -l interface -d 'The network interface to listen on, eg. eth0' -r
complete -c bandwhich -s d -l dns-server -d 'A dns server ip to use instead of the system default' -r
complete -c bandwhich -l log-to -d 'Enable debug logging to a file' -r -F
complete -c bandwhich -s u -l unit-family -d 'Choose a specific family of units' -r -f -a "{bin-bytes\t'bytes, in powers of 2^10',bin-bits\t'bits, in powers of 2^10',si-bytes\t'bytes, in powers of 10^3',si-bits\t'bits, in powers of 10^3'}"
complete -c bandwhich -s r -l raw -d 'Machine friendlier output'
complete -c bandwhich -s n -l no-resolve -d 'Do not attempt to resolve IPs to their hostnames'
complete -c bandwhich -s s -l show-dns -d 'Show DNS queries'
complete -c bandwhich -s v -l verbose -d 'Increase logging verbosity'
complete -c bandwhich -s q -l quiet -d 'Decrease logging verbosity'
complete -c bandwhich -s p -l processes -d 'Show processes table only'
complete -c bandwhich -s c -l connections -d 'Show connections table only'
complete -c bandwhich -s a -l addresses -d 'Show remote addresses table only'
complete -c bandwhich -s t -l total-utilization -d 'Show total (cumulative) usages'
complete -c bandwhich -s h -l help -d 'Print help (see more with \'--help\')'
complete -c bandwhich -s V -l version -d 'Print version'

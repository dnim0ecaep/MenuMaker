
use builtin;
use str;

set edit:completion:arg-completer[bandwhich] = {|@words|
    fn spaces {|n|
        builtin:repeat $n ' ' | str:join ''
    }
    fn cand {|text desc|
        edit:complex-candidate $text &display=$text' '(spaces (- 14 (wcswidth $text)))$desc
    }
    var command = 'bandwhich'
    for word $words[1..-1] {
        if (str:has-prefix $word '-') {
            break
        }
        set command = $command';'$word
    }
    var completions = [
        &'bandwhich'= {
            cand -i 'The network interface to listen on, eg. eth0'
            cand --interface 'The network interface to listen on, eg. eth0'
            cand -d 'A dns server ip to use instead of the system default'
            cand --dns-server 'A dns server ip to use instead of the system default'
            cand --log-to 'Enable debug logging to a file'
            cand -u 'Choose a specific family of units'
            cand --unit-family 'Choose a specific family of units'
            cand -r 'Machine friendlier output'
            cand --raw 'Machine friendlier output'
            cand -n 'Do not attempt to resolve IPs to their hostnames'
            cand --no-resolve 'Do not attempt to resolve IPs to their hostnames'
            cand -s 'Show DNS queries'
            cand --show-dns 'Show DNS queries'
            cand -v 'Increase logging verbosity'
            cand --verbose 'Increase logging verbosity'
            cand -q 'Decrease logging verbosity'
            cand --quiet 'Decrease logging verbosity'
            cand -p 'Show processes table only'
            cand --processes 'Show processes table only'
            cand -c 'Show connections table only'
            cand --connections 'Show connections table only'
            cand -a 'Show remote addresses table only'
            cand --addresses 'Show remote addresses table only'
            cand -t 'Show total (cumulative) usages'
            cand --total-utilization 'Show total (cumulative) usages'
            cand -h 'Print help (see more with ''--help'')'
            cand --help 'Print help (see more with ''--help'')'
            cand -V 'Print version'
            cand --version 'Print version'
        }
    ]
    $completions[$command]
}


using namespace System.Management.Automation
using namespace System.Management.Automation.Language

Register-ArgumentCompleter -Native -CommandName 'bandwhich' -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)

    $commandElements = $commandAst.CommandElements
    $command = @(
        'bandwhich'
        for ($i = 1; $i -lt $commandElements.Count; $i++) {
            $element = $commandElements[$i]
            if ($element -isnot [StringConstantExpressionAst] -or
                $element.StringConstantType -ne [StringConstantType]::BareWord -or
                $element.Value.StartsWith('-') -or
                $element.Value -eq $wordToComplete) {
                break
        }
        $element.Value
    }) -join ';'

    $completions = @(switch ($command) {
        'bandwhich' {
            [CompletionResult]::new('-i', '-i', [CompletionResultType]::ParameterName, 'The network interface to listen on, eg. eth0')
            [CompletionResult]::new('--interface', '--interface', [CompletionResultType]::ParameterName, 'The network interface to listen on, eg. eth0')
            [CompletionResult]::new('-d', '-d', [CompletionResultType]::ParameterName, 'A dns server ip to use instead of the system default')
            [CompletionResult]::new('--dns-server', '--dns-server', [CompletionResultType]::ParameterName, 'A dns server ip to use instead of the system default')
            [CompletionResult]::new('--log-to', '--log-to', [CompletionResultType]::ParameterName, 'Enable debug logging to a file')
            [CompletionResult]::new('-u', '-u', [CompletionResultType]::ParameterName, 'Choose a specific family of units')
            [CompletionResult]::new('--unit-family', '--unit-family', [CompletionResultType]::ParameterName, 'Choose a specific family of units')
            [CompletionResult]::new('-r', '-r', [CompletionResultType]::ParameterName, 'Machine friendlier output')
            [CompletionResult]::new('--raw', '--raw', [CompletionResultType]::ParameterName, 'Machine friendlier output')
            [CompletionResult]::new('-n', '-n', [CompletionResultType]::ParameterName, 'Do not attempt to resolve IPs to their hostnames')
            [CompletionResult]::new('--no-resolve', '--no-resolve', [CompletionResultType]::ParameterName, 'Do not attempt to resolve IPs to their hostnames')
            [CompletionResult]::new('-s', '-s', [CompletionResultType]::ParameterName, 'Show DNS queries')
            [CompletionResult]::new('--show-dns', '--show-dns', [CompletionResultType]::ParameterName, 'Show DNS queries')
            [CompletionResult]::new('-v', '-v', [CompletionResultType]::ParameterName, 'Increase logging verbosity')
            [CompletionResult]::new('--verbose', '--verbose', [CompletionResultType]::ParameterName, 'Increase logging verbosity')
            [CompletionResult]::new('-q', '-q', [CompletionResultType]::ParameterName, 'Decrease logging verbosity')
            [CompletionResult]::new('--quiet', '--quiet', [CompletionResultType]::ParameterName, 'Decrease logging verbosity')
            [CompletionResult]::new('-p', '-p', [CompletionResultType]::ParameterName, 'Show processes table only')
            [CompletionResult]::new('--processes', '--processes', [CompletionResultType]::ParameterName, 'Show processes table only')
            [CompletionResult]::new('-c', '-c', [CompletionResultType]::ParameterName, 'Show connections table only')
            [CompletionResult]::new('--connections', '--connections', [CompletionResultType]::ParameterName, 'Show connections table only')
            [CompletionResult]::new('-a', '-a', [CompletionResultType]::ParameterName, 'Show remote addresses table only')
            [CompletionResult]::new('--addresses', '--addresses', [CompletionResultType]::ParameterName, 'Show remote addresses table only')
            [CompletionResult]::new('-t', '-t', [CompletionResultType]::ParameterName, 'Show total (cumulative) usages')
            [CompletionResult]::new('--total-utilization', '--total-utilization', [CompletionResultType]::ParameterName, 'Show total (cumulative) usages')
            [CompletionResult]::new('-h', '-h', [CompletionResultType]::ParameterName, 'Print help (see more with ''--help'')')
            [CompletionResult]::new('--help', '--help', [CompletionResultType]::ParameterName, 'Print help (see more with ''--help'')')
            [CompletionResult]::new('-V', '-V ', [CompletionResultType]::ParameterName, 'Print version')
            [CompletionResult]::new('--version', '--version', [CompletionResultType]::ParameterName, 'Print version')
            break
        }
    })

    $completions.Where{ $_.CompletionText -like "$wordToComplete*" } |
        Sort-Object -Property ListItemText
}

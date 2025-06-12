
using namespace System.Management.Automation
using namespace System.Management.Automation.Language

Register-ArgumentCompleter -Native -CommandName 'btm' -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)

    $commandElements = $commandAst.CommandElements
    $command = @(
        'btm'
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
        'btm' {
            [CompletionResult]::new('-C', 'C ', [CompletionResultType]::ParameterName, 'Sets the location of the config file.')
            [CompletionResult]::new('--config_location', 'config_location', [CompletionResultType]::ParameterName, 'Sets the location of the config file.')
            [CompletionResult]::new('-t', 't', [CompletionResultType]::ParameterName, 'Default time value for graphs.')
            [CompletionResult]::new('--default_time_value', 'default_time_value', [CompletionResultType]::ParameterName, 'Default time value for graphs.')
            [CompletionResult]::new('--default_widget_count', 'default_widget_count', [CompletionResultType]::ParameterName, 'Sets the N''th selected widget type as the default.')
            [CompletionResult]::new('--default_widget_type', 'default_widget_type', [CompletionResultType]::ParameterName, 'Sets the default widget type. Use --help for more info.')
            [CompletionResult]::new('-r', 'r', [CompletionResultType]::ParameterName, 'Sets how often data is refreshed.')
            [CompletionResult]::new('--rate', 'rate', [CompletionResultType]::ParameterName, 'Sets how often data is refreshed.')
            [CompletionResult]::new('--retention', 'retention', [CompletionResultType]::ParameterName, 'How far back data will be stored up to.')
            [CompletionResult]::new('-d', 'd', [CompletionResultType]::ParameterName, 'The amount of time changed upon zooming.')
            [CompletionResult]::new('--time_delta', 'time_delta', [CompletionResultType]::ParameterName, 'The amount of time changed upon zooming.')
            [CompletionResult]::new('--default_cpu_entry', 'default_cpu_entry', [CompletionResultType]::ParameterName, 'Sets which CPU entry type is selected by default.')
            [CompletionResult]::new('--memory_legend', 'memory_legend', [CompletionResultType]::ParameterName, 'Where to place the legend for the memory chart widget.')
            [CompletionResult]::new('--network_legend', 'network_legend', [CompletionResultType]::ParameterName, 'Where to place the legend for the network chart widget.')
            [CompletionResult]::new('--theme', 'theme', [CompletionResultType]::ParameterName, 'Use a built-in color theme, use ''--help'' for info on the colors. [possible values: default, default-light, gruvbox, gruvbox-light, nord, nord-light]')
            [CompletionResult]::new('--autohide_time', 'autohide_time', [CompletionResultType]::ParameterName, 'Temporarily shows the time scale in graphs.')
            [CompletionResult]::new('-b', 'b', [CompletionResultType]::ParameterName, 'Hides graphs and uses a more basic look.')
            [CompletionResult]::new('--basic', 'basic', [CompletionResultType]::ParameterName, 'Hides graphs and uses a more basic look.')
            [CompletionResult]::new('--disable_click', 'disable_click', [CompletionResultType]::ParameterName, 'Disables mouse clicks.')
            [CompletionResult]::new('-m', 'm', [CompletionResultType]::ParameterName, 'Uses a dot marker for graphs.')
            [CompletionResult]::new('--dot_marker', 'dot_marker', [CompletionResultType]::ParameterName, 'Uses a dot marker for graphs.')
            [CompletionResult]::new('-e', 'e', [CompletionResultType]::ParameterName, 'Expand the default widget upon starting the app.')
            [CompletionResult]::new('--expanded', 'expanded', [CompletionResultType]::ParameterName, 'Expand the default widget upon starting the app.')
            [CompletionResult]::new('--hide_table_gap', 'hide_table_gap', [CompletionResultType]::ParameterName, 'Hides spacing between table headers and entries.')
            [CompletionResult]::new('--hide_time', 'hide_time', [CompletionResultType]::ParameterName, 'Hides the time scale from being shown.')
            [CompletionResult]::new('--show_table_scroll_position', 'show_table_scroll_position', [CompletionResultType]::ParameterName, 'Shows the list scroll position tracker in the widget title for table widgets.')
            [CompletionResult]::new('-S', 'S ', [CompletionResultType]::ParameterName, 'Enables case sensitivity by default.')
            [CompletionResult]::new('--case_sensitive', 'case_sensitive', [CompletionResultType]::ParameterName, 'Enables case sensitivity by default.')
            [CompletionResult]::new('-u', 'u', [CompletionResultType]::ParameterName, 'Calculates process CPU usage as a percentage of current usage rather than total usage.')
            [CompletionResult]::new('--current_usage', 'current_usage', [CompletionResultType]::ParameterName, 'Calculates process CPU usage as a percentage of current usage rather than total usage.')
            [CompletionResult]::new('--disable_advanced_kill', 'disable_advanced_kill', [CompletionResultType]::ParameterName, 'Hides additional stopping options Unix-like systems.')
            [CompletionResult]::new('-g', 'g', [CompletionResultType]::ParameterName, 'Groups processes with the same name by default.')
            [CompletionResult]::new('--group_processes', 'group_processes', [CompletionResultType]::ParameterName, 'Groups processes with the same name by default.')
            [CompletionResult]::new('--process_memory_as_value', 'process_memory_as_value', [CompletionResultType]::ParameterName, 'Defaults to showing process memory usage by value.')
            [CompletionResult]::new('--process_command', 'process_command', [CompletionResultType]::ParameterName, 'Shows the full command name instead of the process name by default.')
            [CompletionResult]::new('-R', 'R ', [CompletionResultType]::ParameterName, 'Enables regex by default while searching.')
            [CompletionResult]::new('--regex', 'regex', [CompletionResultType]::ParameterName, 'Enables regex by default while searching.')
            [CompletionResult]::new('-T', 'T ', [CompletionResultType]::ParameterName, 'Makes the process widget use tree mode by default.')
            [CompletionResult]::new('--tree', 'tree', [CompletionResultType]::ParameterName, 'Makes the process widget use tree mode by default.')
            [CompletionResult]::new('-n', 'n', [CompletionResultType]::ParameterName, 'Show process CPU% usage without averaging over the number of CPU cores.')
            [CompletionResult]::new('--unnormalized_cpu', 'unnormalized_cpu', [CompletionResultType]::ParameterName, 'Show process CPU% usage without averaging over the number of CPU cores.')
            [CompletionResult]::new('-W', 'W ', [CompletionResultType]::ParameterName, 'Enables whole-word matching by default while searching.')
            [CompletionResult]::new('--whole_word', 'whole_word', [CompletionResultType]::ParameterName, 'Enables whole-word matching by default while searching.')
            [CompletionResult]::new('-c', 'c', [CompletionResultType]::ParameterName, 'Use Celsius as the temperature unit. Default.')
            [CompletionResult]::new('--celsius', 'celsius', [CompletionResultType]::ParameterName, 'Use Celsius as the temperature unit. Default.')
            [CompletionResult]::new('-f', 'f', [CompletionResultType]::ParameterName, 'Use Fahrenheit as the temperature unit.')
            [CompletionResult]::new('--fahrenheit', 'fahrenheit', [CompletionResultType]::ParameterName, 'Use Fahrenheit as the temperature unit.')
            [CompletionResult]::new('-k', 'k', [CompletionResultType]::ParameterName, 'Use Kelvin as the temperature unit.')
            [CompletionResult]::new('--kelvin', 'kelvin', [CompletionResultType]::ParameterName, 'Use Kelvin as the temperature unit.')
            [CompletionResult]::new('-l', 'l', [CompletionResultType]::ParameterName, 'Puts the CPU chart legend on the left side.')
            [CompletionResult]::new('--cpu_left_legend', 'cpu_left_legend', [CompletionResultType]::ParameterName, 'Puts the CPU chart legend on the left side.')
            [CompletionResult]::new('-a', 'a', [CompletionResultType]::ParameterName, 'Hides the average CPU usage entry.')
            [CompletionResult]::new('--hide_avg_cpu', 'hide_avg_cpu', [CompletionResultType]::ParameterName, 'Hides the average CPU usage entry.')
            [CompletionResult]::new('--enable_cache_memory', 'enable_cache_memory', [CompletionResultType]::ParameterName, 'Enables collecting and displaying cache and buffer memory.')
            [CompletionResult]::new('--network_use_bytes', 'network_use_bytes', [CompletionResultType]::ParameterName, 'Displays the network widget using bytes.')
            [CompletionResult]::new('--network_use_binary_prefix', 'network_use_binary_prefix', [CompletionResultType]::ParameterName, 'Displays the network widget with binary prefixes.')
            [CompletionResult]::new('--network_use_log', 'network_use_log', [CompletionResultType]::ParameterName, 'Displays the network widget with a log scale.')
            [CompletionResult]::new('--use_old_network_legend', 'use_old_network_legend', [CompletionResultType]::ParameterName, '(DEPRECATED) Uses a separate network legend.')
            [CompletionResult]::new('--battery', 'battery', [CompletionResultType]::ParameterName, 'Shows the battery widget in non-custom layouts.')
            [CompletionResult]::new('--enable_gpu', 'enable_gpu', [CompletionResultType]::ParameterName, 'Enable collecting and displaying GPU usage.')
            [CompletionResult]::new('-h', 'h', [CompletionResultType]::ParameterName, 'Prints help info (for more details use ''--help''.')
            [CompletionResult]::new('--help', 'help', [CompletionResultType]::ParameterName, 'Prints help info (for more details use ''--help''.')
            [CompletionResult]::new('-V', 'V ', [CompletionResultType]::ParameterName, 'Prints version information.')
            [CompletionResult]::new('--version', 'version', [CompletionResultType]::ParameterName, 'Prints version information.')
            break
        }
    })

    $completions.Where{ $_.CompletionText -like "$wordToComplete*" } |
        Sort-Object -Property ListItemText
}

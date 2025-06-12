
use builtin;
use str;

set edit:completion:arg-completer[btm] = {|@words|
    fn spaces {|n|
        builtin:repeat $n ' ' | str:join ''
    }
    fn cand {|text desc|
        edit:complex-candidate $text &display=$text' '(spaces (- 14 (wcswidth $text)))$desc
    }
    var command = 'btm'
    for word $words[1..-1] {
        if (str:has-prefix $word '-') {
            break
        }
        set command = $command';'$word
    }
    var completions = [
        &'btm'= {
            cand -C 'Sets the location of the config file.'
            cand --config_location 'Sets the location of the config file.'
            cand -t 'Default time value for graphs.'
            cand --default_time_value 'Default time value for graphs.'
            cand --default_widget_count 'Sets the N''th selected widget type as the default.'
            cand --default_widget_type 'Sets the default widget type. Use --help for more info.'
            cand -r 'Sets how often data is refreshed.'
            cand --rate 'Sets how often data is refreshed.'
            cand --retention 'How far back data will be stored up to.'
            cand -d 'The amount of time changed upon zooming.'
            cand --time_delta 'The amount of time changed upon zooming.'
            cand --default_cpu_entry 'Sets which CPU entry type is selected by default.'
            cand --memory_legend 'Where to place the legend for the memory chart widget.'
            cand --network_legend 'Where to place the legend for the network chart widget.'
            cand --theme 'Use a built-in color theme, use ''--help'' for info on the colors. [possible values: default, default-light, gruvbox, gruvbox-light, nord, nord-light]'
            cand --autohide_time 'Temporarily shows the time scale in graphs.'
            cand -b 'Hides graphs and uses a more basic look.'
            cand --basic 'Hides graphs and uses a more basic look.'
            cand --disable_click 'Disables mouse clicks.'
            cand -m 'Uses a dot marker for graphs.'
            cand --dot_marker 'Uses a dot marker for graphs.'
            cand -e 'Expand the default widget upon starting the app.'
            cand --expanded 'Expand the default widget upon starting the app.'
            cand --hide_table_gap 'Hides spacing between table headers and entries.'
            cand --hide_time 'Hides the time scale from being shown.'
            cand --show_table_scroll_position 'Shows the list scroll position tracker in the widget title for table widgets.'
            cand -S 'Enables case sensitivity by default.'
            cand --case_sensitive 'Enables case sensitivity by default.'
            cand -u 'Calculates process CPU usage as a percentage of current usage rather than total usage.'
            cand --current_usage 'Calculates process CPU usage as a percentage of current usage rather than total usage.'
            cand --disable_advanced_kill 'Hides additional stopping options Unix-like systems.'
            cand -g 'Groups processes with the same name by default.'
            cand --group_processes 'Groups processes with the same name by default.'
            cand --process_memory_as_value 'Defaults to showing process memory usage by value.'
            cand --process_command 'Shows the full command name instead of the process name by default.'
            cand -R 'Enables regex by default while searching.'
            cand --regex 'Enables regex by default while searching.'
            cand -T 'Makes the process widget use tree mode by default.'
            cand --tree 'Makes the process widget use tree mode by default.'
            cand -n 'Show process CPU% usage without averaging over the number of CPU cores.'
            cand --unnormalized_cpu 'Show process CPU% usage without averaging over the number of CPU cores.'
            cand -W 'Enables whole-word matching by default while searching.'
            cand --whole_word 'Enables whole-word matching by default while searching.'
            cand -c 'Use Celsius as the temperature unit. Default.'
            cand --celsius 'Use Celsius as the temperature unit. Default.'
            cand -f 'Use Fahrenheit as the temperature unit.'
            cand --fahrenheit 'Use Fahrenheit as the temperature unit.'
            cand -k 'Use Kelvin as the temperature unit.'
            cand --kelvin 'Use Kelvin as the temperature unit.'
            cand -l 'Puts the CPU chart legend on the left side.'
            cand --cpu_left_legend 'Puts the CPU chart legend on the left side.'
            cand -a 'Hides the average CPU usage entry.'
            cand --hide_avg_cpu 'Hides the average CPU usage entry.'
            cand --enable_cache_memory 'Enables collecting and displaying cache and buffer memory.'
            cand --network_use_bytes 'Displays the network widget using bytes.'
            cand --network_use_binary_prefix 'Displays the network widget with binary prefixes.'
            cand --network_use_log 'Displays the network widget with a log scale.'
            cand --use_old_network_legend '(DEPRECATED) Uses a separate network legend.'
            cand --battery 'Shows the battery widget in non-custom layouts.'
            cand --enable_gpu 'Enable collecting and displaying GPU usage.'
            cand -h 'Prints help info (for more details use ''--help''.'
            cand --help 'Prints help info (for more details use ''--help''.'
            cand -V 'Prints version information.'
            cand --version 'Prints version information.'
        }
    ]
    $completions[$command]
}

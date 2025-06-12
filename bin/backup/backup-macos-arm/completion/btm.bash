_btm() {
    local i cur prev opts cmd
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cmd=""
    opts=""

    for i in ${COMP_WORDS[@]}
    do
        case "${cmd},${i}" in
            ",$1")
                cmd="btm"
                ;;
            *)
                ;;
        esac
    done

    case "${cmd}" in
        btm)
            opts="-b -C -t -m -e -r -d -S -u -g -R -T -n -W -c -f -k -l -a -h -V --autohide_time --basic --config_location --default_time_value --default_widget_count --default_widget_type --disable_click --dot_marker --expanded --hide_table_gap --hide_time --rate --retention --show_table_scroll_position --time_delta --case_sensitive --current_usage --disable_advanced_kill --group_processes --process_memory_as_value --process_command --regex --tree --unnormalized_cpu --whole_word --celsius --fahrenheit --kelvin --cpu_left_legend --default_cpu_entry --hide_avg_cpu --memory_legend --enable_cache_memory --network_legend --network_use_bytes --network_use_binary_prefix --network_use_log --use_old_network_legend --battery --enable_gpu --theme --help --version"
            if [[ ${cur} == -* || ${COMP_CWORD} -eq 1 ]] ; then
                COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
                return 0
            fi
            case "${prev}" in
                --config_location)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                -C)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --default_time_value)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                -t)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --default_widget_count)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --default_widget_type)
                    COMPREPLY=($(compgen -W "cpu mem net network proc process processes temp temperature disk batt battery" -- "${cur}"))
                    return 0
                    ;;
                --rate)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                -r)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --retention)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --time_delta)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                -d)
                    COMPREPLY=($(compgen -f "${cur}"))
                    return 0
                    ;;
                --default_cpu_entry)
                    COMPREPLY=($(compgen -W "all avg" -- "${cur}"))
                    return 0
                    ;;
                --memory_legend)
                    COMPREPLY=($(compgen -W "none top-left top top-right left right bottom-left bottom bottom-right" -- "${cur}"))
                    return 0
                    ;;
                --network_legend)
                    COMPREPLY=($(compgen -W "none top-left top top-right left right bottom-left bottom bottom-right" -- "${cur}"))
                    return 0
                    ;;
                --theme)
                    COMPREPLY=($(compgen -W "default default-light gruvbox gruvbox-light nord nord-light" -- "${cur}"))
                    return 0
                    ;;
                *)
                    COMPREPLY=()
                    ;;
            esac
            COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
            return 0
            ;;
    esac
}

if [[ "${BASH_VERSINFO[0]}" -eq 4 && "${BASH_VERSINFO[1]}" -ge 4 || "${BASH_VERSINFO[0]}" -gt 4 ]]; then
    complete -F _btm -o nosort -o bashdefault -o default btm
else
    complete -F _btm -o bashdefault -o default btm
fi

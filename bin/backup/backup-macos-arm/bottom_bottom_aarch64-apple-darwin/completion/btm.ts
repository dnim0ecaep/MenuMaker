const completion: Fig.Spec = {
  name: "btm",
  description: "A customizable cross-platform graphical process/system monitor for the terminal. Supports Linux, macOS, and Windows.",
  options: [
    {
      name: ["-C", "--config_location"],
      description: "Sets the location of the config file.",
      isRepeatable: true,
      args: {
        name: "config_location",
        isOptional: true,
        template: "filepaths",
      },
    },
    {
      name: ["-t", "--default_time_value"],
      description: "Default time value for graphs.",
      isRepeatable: true,
      args: {
        name: "default_time_value",
        isOptional: true,
      },
    },
    {
      name: "--default_widget_count",
      description: "Sets the N'th selected widget type as the default.",
      isRepeatable: true,
      args: {
        name: "default_widget_count",
        isOptional: true,
      },
    },
    {
      name: "--default_widget_type",
      description: "Sets the default widget type. Use --help for more info.",
      isRepeatable: true,
      args: {
        name: "default_widget_type",
        isOptional: true,
        suggestions: [
          "cpu",
          "mem",
          "net",
          "network",
          "proc",
          "process",
          "processes",
          "temp",
          "temperature",
          "disk",
          "batt",
          "battery",
        ],
      },
    },
    {
      name: ["-r", "--rate"],
      description: "Sets how often data is refreshed.",
      isRepeatable: true,
      args: {
        name: "rate",
        isOptional: true,
      },
    },
    {
      name: "--retention",
      description: "How far back data will be stored up to.",
      isRepeatable: true,
      args: {
        name: "retention",
        isOptional: true,
      },
    },
    {
      name: ["-d", "--time_delta"],
      description: "The amount of time changed upon zooming.",
      isRepeatable: true,
      args: {
        name: "time_delta",
        isOptional: true,
      },
    },
    {
      name: "--default_cpu_entry",
      description: "Sets which CPU entry type is selected by default.",
      isRepeatable: true,
      args: {
        name: "default_cpu_entry",
        isOptional: true,
        suggestions: [
          "all",
          "avg",
        ],
      },
    },
    {
      name: "--memory_legend",
      description: "Where to place the legend for the memory chart widget.",
      isRepeatable: true,
      args: {
        name: "memory_legend",
        isOptional: true,
        suggestions: [
          "none",
          "top-left",
          "top",
          "top-right",
          "left",
          "right",
          "bottom-left",
          "bottom",
          "bottom-right",
        ],
      },
    },
    {
      name: "--network_legend",
      description: "Where to place the legend for the network chart widget.",
      isRepeatable: true,
      args: {
        name: "network_legend",
        isOptional: true,
        suggestions: [
          "none",
          "top-left",
          "top",
          "top-right",
          "left",
          "right",
          "bottom-left",
          "bottom",
          "bottom-right",
        ],
      },
    },
    {
      name: "--theme",
      description: "Use a built-in color theme, use '--help' for info on the colors. [possible values: default, default-light, gruvbox, gruvbox-light, nord, nord-light]",
      isRepeatable: true,
      args: {
        name: "theme",
        isOptional: true,
        suggestions: [
          "default",
          "default-light",
          "gruvbox",
          "gruvbox-light",
          "nord",
          "nord-light",
        ],
      },
    },
    {
      name: "--autohide_time",
      description: "Temporarily shows the time scale in graphs.",
    },
    {
      name: ["-b", "--basic"],
      description: "Hides graphs and uses a more basic look.",
    },
    {
      name: "--disable_click",
      description: "Disables mouse clicks.",
    },
    {
      name: ["-m", "--dot_marker"],
      description: "Uses a dot marker for graphs.",
    },
    {
      name: ["-e", "--expanded"],
      description: "Expand the default widget upon starting the app.",
    },
    {
      name: "--hide_table_gap",
      description: "Hides spacing between table headers and entries.",
    },
    {
      name: "--hide_time",
      description: "Hides the time scale from being shown.",
    },
    {
      name: "--show_table_scroll_position",
      description: "Shows the list scroll position tracker in the widget title for table widgets.",
    },
    {
      name: ["-S", "--case_sensitive"],
      description: "Enables case sensitivity by default.",
    },
    {
      name: ["-u", "--current_usage"],
      description: "Calculates process CPU usage as a percentage of current usage rather than total usage.",
    },
    {
      name: "--disable_advanced_kill",
      description: "Hides additional stopping options Unix-like systems.",
    },
    {
      name: ["-g", "--group_processes"],
      description: "Groups processes with the same name by default.",
    },
    {
      name: "--process_memory_as_value",
      description: "Defaults to showing process memory usage by value.",
    },
    {
      name: "--process_command",
      description: "Shows the full command name instead of the process name by default.",
    },
    {
      name: ["-R", "--regex"],
      description: "Enables regex by default while searching.",
    },
    {
      name: ["-T", "--tree"],
      description: "Makes the process widget use tree mode by default.",
    },
    {
      name: ["-n", "--unnormalized_cpu"],
      description: "Show process CPU% usage without averaging over the number of CPU cores.",
    },
    {
      name: ["-W", "--whole_word"],
      description: "Enables whole-word matching by default while searching.",
    },
    {
      name: ["-c", "--celsius"],
      description: "Use Celsius as the temperature unit. Default.",
    },
    {
      name: ["-f", "--fahrenheit"],
      description: "Use Fahrenheit as the temperature unit.",
    },
    {
      name: ["-k", "--kelvin"],
      description: "Use Kelvin as the temperature unit.",
    },
    {
      name: ["-l", "--cpu_left_legend"],
      description: "Puts the CPU chart legend on the left side.",
    },
    {
      name: ["-a", "--hide_avg_cpu"],
      description: "Hides the average CPU usage entry.",
    },
    {
      name: "--enable_cache_memory",
      description: "Enables collecting and displaying cache and buffer memory.",
    },
    {
      name: "--network_use_bytes",
      description: "Displays the network widget using bytes.",
    },
    {
      name: "--network_use_binary_prefix",
      description: "Displays the network widget with binary prefixes.",
    },
    {
      name: "--network_use_log",
      description: "Displays the network widget with a log scale.",
    },
    {
      name: "--use_old_network_legend",
      description: "(DEPRECATED) Uses a separate network legend.",
    },
    {
      name: "--battery",
      description: "Shows the battery widget in non-custom layouts.",
    },
    {
      name: "--enable_gpu",
      description: "Enable collecting and displaying GPU usage.",
    },
    {
      name: ["-h", "--help"],
      description: "Prints help info (for more details use '--help'.",
    },
    {
      name: ["-V", "--version"],
      description: "Prints version information.",
    },
  ],
};

export default completion;

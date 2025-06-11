#!/usr/bin/env python3
"""
Menu Maker - Enhanced categorized menu system
Features: Categories, Info display, Collapse/Expand, Theme selection
"""

import os
import subprocess
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container, ScrollableContainer
from textual.widgets import Header, Footer, Static, Button, Input, Label, TextArea, Checkbox
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive


class InfoScreen(Screen):
    """Screen for displaying app information."""
    
    BINDINGS = [
        Binding("escape,i,enter", "close", "Close"),
    ]
    
    def __init__(self, item_data: Dict[str, str]):
        super().__init__()
        self.item_data = item_data
    
    def compose(self) -> ComposeResult:
        """Create info screen layout."""
        with Container(classes="info-container"):
            yield Label("Application Information", classes="info-title")
            yield Label(f"Label: {self.item_data.get('label', 'N/A')}", classes="info-field")
            yield Label(f"Command: {self.item_data.get('cmd', 'N/A')}", classes="info-field")
            yield Label(f"Category: {self.item_data.get('category', 'N/A')}", classes="info-field")
            yield Label("", classes="info-spacer")
            yield Label("Description:", classes="info-label")
            yield Label(f"{self.item_data.get('info', 'No description available')}", classes="info-description")
            yield Label("", classes="info-spacer")
            with Horizontal(classes="button-row"):
                yield Button("Close", id="close", variant="primary")
    
    def action_close(self) -> None:
        """Close the info screen."""
        self.dismiss()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "close":
            self.dismiss()


class EditTitleScreen(Screen):
    """Screen for editing the application title."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+s", "save", "Save"),
    ]
    
    def __init__(self, current_title: str):
        super().__init__()
        self.current_title = current_title
    
    def compose(self) -> ComposeResult:
        """Create title edit screen layout."""
        with Container(classes="edit-container"):
            yield Label("Edit Application Title", classes="edit-title")
            
            yield Label("Application Title:")
            yield Input(value=self.current_title, id="title_input")
            
            with Horizontal(classes="button-row"):
                yield Button("Save", id="save", variant="primary")
                yield Button("Cancel", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()
    
    def action_save(self) -> None:
        """Save the title."""
        title_input = self.query_one("#title_input", Input)
        new_title = title_input.value.strip()
        
        if new_title:
            self.dismiss({"action": "save", "title": new_title})
        else:
            self.dismiss({"action": "cancel"})
    
    def action_cancel(self) -> None:
        """Cancel editing."""
        self.dismiss({"action": "cancel"})


class EditCategoryScreen(Screen):
    """Screen for editing category names."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+s", "save", "Save"),
    ]
    
    def __init__(self, old_category_name: str):
        super().__init__()
        self.old_category_name = old_category_name
    
    def compose(self) -> ComposeResult:
        """Create category edit screen layout."""
        with Container(classes="edit-container"):
            yield Label("Edit Category Name", classes="edit-title")
            
            yield Label("Category Name:")
            yield Input(value=self.old_category_name, id="category_input")
            
            with Horizontal(classes="button-row"):
                yield Button("Save", id="save", variant="primary")
                yield Button("Cancel", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()
    
    def action_save(self) -> None:
        """Save the category name."""
        category_input = self.query_one("#category_input", Input)
        new_name = category_input.value.strip()
        
        if new_name and new_name != self.old_category_name:
            self.dismiss({"action": "save", "old_name": self.old_category_name, "new_name": new_name})
        else:
            self.dismiss({"action": "cancel"})
    
    def action_cancel(self) -> None:
        """Cancel editing."""
        self.dismiss({"action": "cancel"})


class EditItemScreen(Screen):
    """Screen for editing menu items with all fields."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+s", "save", "Save"),
    ]
    
    def __init__(self, item_data: Dict[str, str], categories: List[str], item_index: int = -1):
        super().__init__()
        self.item_data = item_data.copy()
        self.categories = categories
        self.item_index = item_index
        self.current_category_index = 0
        
        # Set default category index
        if self.item_data.get('category') in categories:
            self.current_category_index = categories.index(self.item_data['category'])
    
    def compose(self) -> ComposeResult:
        """Create edit screen layout."""
        with Container(classes="edit-container"):
            title = "Edit Item" if self.item_index >= 0 else "New Item"
            yield Label(title, classes="edit-title")
            
            yield Label("Label:")
            yield Input(value=self.item_data.get('label', ''), id="label_input")
            
            yield Label("Command:")
            yield Input(value=self.item_data.get('cmd', ''), id="cmd_input")
            
            yield Label("Info/Description:")
            yield TextArea(text=self.item_data.get('info', ''), id="info_input")
            
            yield Label("Category:")
            yield Input(value=self.item_data.get('category', self.categories[0] if self.categories else 'General'), id="category_input")
            
            yield Label("Pause before returning to menu:")
            pause_value = self.item_data.get('pause', False)
            if isinstance(pause_value, str):
                pause_value = pause_value.lower() in ('true', 'yes', '1')
            yield Checkbox("Pause and wait for keypress", value=pause_value, id="pause_checkbox")
            
            with Horizontal(classes="button-row"):
                yield Button("Save", id="save", variant="primary")
                yield Button("Cancel", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()
    
    def action_save(self) -> None:
        """Save the item data."""
        label_input = self.query_one("#label_input", Input)
        cmd_input = self.query_one("#cmd_input", Input)
        info_input = self.query_one("#info_input", TextArea)
        category_input = self.query_one("#category_input", Input)
        pause_checkbox = self.query_one("#pause_checkbox", Checkbox)
        
        result_data = {
            "label": label_input.value.strip(),
            "cmd": cmd_input.value.strip(),
            "info": info_input.text.strip(),
            "category": category_input.value.strip() or "General",
            "pause": pause_checkbox.value
        }
        
        self.dismiss({"action": "save", "data": result_data, "index": self.item_index})
    
    def action_cancel(self) -> None:
        """Cancel editing."""
        self.dismiss({"action": "cancel"})


class ThemeSelectionScreen(Screen):
    """Screen for selecting application themes."""
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "apply", "Apply Theme"),
        Binding("up", "cursor_up", "Up"),
        Binding("down", "cursor_down", "Down"),
    ]
    
    THEMES = {
        "classic": {
            "name": "Classic Teal",
            "primary": "#00b4d8",
            "accent": "#00f5ff", 
            "bg": "#034e68",
            "surface": "#023047",
            "text": "#caf0f8"
        },
        "nord": {
            "name": "Nord Theme",
            "primary": "#5e81ac",
            "accent": "#88c0d0",
            "bg": "#2e3440",
            "surface": "#3b4252",
            "text": "#eceff4"
        },
        "gruvbox": {
            "name": "Gruvbox Dark",
            "primary": "#d79921",
            "accent": "#fabd2f",
            "bg": "#282828",
            "surface": "#3c3836",
            "text": "#fbf1c7"
        },
        "dracula": {
            "name": "Dracula",
            "primary": "#bd93f9",
            "accent": "#ff79c6",
            "bg": "#282a36",
            "surface": "#44475a",
            "text": "#f8f8f2"
        },
        "monokai": {
            "name": "Monokai",
            "primary": "#a6e22e",
            "accent": "#f92672",
            "bg": "#272822",
            "surface": "#383830",
            "text": "#f8f8f2"
        }
    }
    
    def __init__(self, current_theme: str = "classic"):
        super().__init__()
        self.current_theme = current_theme
        self.selected_index = 0
        self.theme_keys = list(self.THEMES.keys())
        if current_theme in self.theme_keys:
            self.selected_index = self.theme_keys.index(current_theme)
    
    def compose(self) -> ComposeResult:
        """Create theme selection screen layout."""
        with Container(classes="edit-container"):
            yield Label("Choose Theme", classes="edit-title")
            
            with Container():
                for i, (theme_key, theme_data) in enumerate(self.THEMES.items()):
                    selected_marker = "▶ " if i == self.selected_index else "  "
                    yield Label(f"{selected_marker}{theme_data['name']}", id=f"theme_{i}")
            
            with Horizontal(classes="button-row"):
                yield Button("Apply Theme", id="apply", variant="primary")
                yield Button("Cancel", id="cancel", variant="default")
    
    def action_cursor_up(self) -> None:
        """Move selection up."""
        self.selected_index = max(0, self.selected_index - 1)
        self.update_selection()
    
    def action_cursor_down(self) -> None:
        """Move selection down."""
        self.selected_index = min(len(self.theme_keys) - 1, self.selected_index + 1)
        self.update_selection()
    
    def action_apply(self) -> None:
        """Apply selected theme."""
        selected_theme = self.theme_keys[self.selected_index]
        self.dismiss({"action": "apply", "theme": selected_theme})
    
    def action_cancel(self) -> None:
        """Cancel theme selection."""
        self.dismiss({"action": "cancel"})
    
    def update_selection(self) -> None:
        """Update visual selection."""
        for i, theme_key in enumerate(self.theme_keys):
            label = self.query_one(f"#theme_{i}", Label)
            theme_data = self.THEMES[theme_key]
            selected_marker = "▶ " if i == self.selected_index else "  "
            label.update(f"{selected_marker}{theme_data['name']}")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "apply":
            self.action_apply()
        elif event.button.id == "cancel":
            self.action_cancel()


class MenuMaker(App):
    """Menu Maker - Enhanced categorized menu system."""
    
    CSS = """
    Screen {
        background: #023047;
    }
    
    Header {
        background: #00b4d8;
        color: white;
        text-align: center;
        height: 3;
    }
    
    Footer {
        background: #00b4d8;
        color: #caf0f8;
        height: 3;
    }
    
    .main-container {
        height: 1fr;
        border: solid #00b4d8;
        background: #034e68;
        padding: 0;
    }
    
    .status-bar {
        dock: top;
        height: 3;
        background: #0077b6;
        color: #caf0f8;
        text-align: center;
        padding: 1;
    }
    
    .menu-container {
        height: 1fr;
        border: solid #00b4d8;
        background: #034e68;
        padding: 1;
        margin: 0;
        overflow-y: auto;
    }
    
    .category-header {
        height: 2;
        padding: 0 1;
        margin: 0;
        background: #034e68;
        color: #caf0f8;
        text-style: bold;
        border: none;
    }
    
    .category-header.-selected {
        background: #00f5ff;
        color: #023047;
    }
    
    .menu-item {
        height: 2;
        padding: 0 2;
        margin: 0;
        background: #034e68;
        color: #caf0f8;
        border: none;
    }
    
    .menu-item.-selected {
        background: #00f5ff;
        color: #023047;
        text-style: bold;
    }
    
    .info-container {
        align: center middle;
        width: 70;
        height: auto;
        background: #034e68;
        border: solid #00f5ff;
        padding: 2;
    }
    
    .info-title {
        text-align: center;
        text-style: bold;
        color: #00f5ff;
        margin-bottom: 1;
    }
    
    .info-field {
        color: #caf0f8;
        margin-bottom: 1;
    }
    
    .info-description {
        color: #caf0f8;
        text-style: italic;
        margin-bottom: 1;
    }
    
    .edit-container {
        align: center middle;
        width: 80;
        height: auto;
        background: #034e68;
        border: solid #00f5ff;
        padding: 2;
    }
    
    .edit-title {
        text-align: center;
        text-style: bold;
        color: #00f5ff;
        margin-bottom: 1;
    }
    
    .theme-editor-container {
        width: 1fr;
        height: 1fr;
        background: #034e68;
        padding: 2;
    }
    
    .theme-editor-title {
        text-align: center;
        text-style: bold;
        color: #00f5ff;
        height: 3;
    }
    
    .theme-option {
        height: 4;
        border: solid #00b4d8;
        margin-bottom: 1;
        padding: 1;
    }
    
    .button-row {
        align: center middle;
        height: auto;
        margin-top: 1;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    TITLE = "Menu Maker"
    SUB_TITLE = "Enhanced Categorized Menu System"
    
    BINDINGS = [
        Binding("q,escape", "exit_app", "Exit", priority=True),
        Binding("e", "edit_item", "Edit", show=True),
        Binding("enter", "execute_item", "Execute", show=True),
        Binding("n", "new_item", "New Item", show=True),
        Binding("d", "delete_item", "Delete", show=True),
        Binding("t", "change_theme", "Theme", show=True),
        Binding("ctrl+t", "edit_title", "Edit Title", show=True),
        Binding("i", "show_info", "Info", show=True),
        Binding("space", "toggle_category", "Toggle Category", show=True),
        # Enhanced key bindings for Linux compatibility
        Binding("up,k", "cursor_up", "Up", show=False),
        Binding("down,j", "cursor_down", "Down", show=False),
        Binding("tab", "cursor_down", "Next", show=False),
        Binding("shift+tab", "cursor_up", "Previous", show=False),
        # Additional Linux-specific navigation keys
        Binding("ctrl+p", "cursor_up", "Up Alt", show=False),
        Binding("ctrl+n", "cursor_down", "Down Alt", show=False),
        Binding("ctrl+b", "scan_bin_directory", "Scan ./bin", show=True),
    ]
    
    # Reactive state
    current_index = reactive(0)
    menu_data = reactive({})
    
    def __init__(self):
        super().__init__()
        self.menu_widgets = []
        self.display_items = []  # Flattened list for navigation
        self.status_bar = None
        self.menu_container = None
        self.config_file = Path("menus.json")
        self.app_theme = "classic"
        self.app_title = "Menu Maker — Enhanced Categorized Menu System"
        
        # Linux/Debian compatibility detection
        self.is_linux_system = self.detect_linux_system()
        self.terminal_type = self.detect_terminal_type()
        
        self.load_menu_data()
    
    def detect_linux_system(self) -> bool:
        """Detect if running on Linux system."""
        try:
            return os.name == 'posix' and 'linux' in os.uname().sysname.lower()
        except:
            return False
    
    def detect_terminal_type(self) -> str:
        """Detect terminal type for compatibility adjustments."""
        try:
            term = os.environ.get('TERM', '').lower()
            term_program = os.environ.get('TERM_PROGRAM', '').lower()
            
            if 'xterm' in term or 'gnome' in term_program:
                return 'xterm'
            elif 'screen' in term:
                return 'screen'
            elif 'tmux' in term:
                return 'tmux'
            elif 'linux' in term:
                return 'linux_console'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    def load_menu_data(self) -> None:
        """Load menu data from JSON file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.menu_data = data.get('categories', {})
                    # Load saved settings if available
                    if 'app_settings' in data:
                        settings = data['app_settings']
                        if 'theme' in settings:
                            self.app_theme = settings['theme']
                            self.apply_theme(self.app_theme)
                        if 'title' in settings:
                            self.app_title = settings['title']
            else:
                self.create_default_menu()
        except Exception as e:
            self.create_default_menu()
    
    def create_default_menu(self) -> None:
        """Create default categorized menu structure."""
        default_data = {
            "System Tools": {
                "expanded": True,
                "items": [
                    {"label": "System Monitor", "cmd": "htop", "info": "Interactive process viewer", "category": "System Tools"}
                ]
            }
        }
        self.menu_data = default_data
        self.save_menu_data()
    
    def save_menu_data(self) -> None:
        """Save menu data to JSON file."""
        try:
            data = {
                "categories": self.menu_data,
                "app_settings": {
                    "theme": self.app_theme,
                    "title": self.app_title
                }
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            pass  # Silently handle save errors
    
    def compose(self) -> ComposeResult:
        """Create the application layout."""
        self.header = Header()
        yield self.header
        
        with Container(classes="main-container"):
            self.status_bar = Static("", classes="status-bar")
            yield self.status_bar
            
            with ScrollableContainer(classes="menu-container") as container:
                self.menu_container = container
                # Menu items will be populated in update_menu_display
                pass
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize after mounting."""
        self.update_title()
        self.update_menu_display()
        self.update_status()
        # Ensure proper initial index setting
        object.__setattr__(self, 'current_index', 0)
    
    def update_menu_display(self) -> None:
        """Update menu display with categories and items."""
        if not self.menu_container:
            return
        
        # Clear existing widgets
        self.menu_container.remove_children()
        self.menu_widgets.clear()
        self.display_items.clear()
        
        # Remove empty categories first
        self.cleanup_empty_categories()
        
        # Build flattened display list and widgets
        total_items = 0
        for category_name, category_data in self.menu_data.items():
            # Add category header with proper prefix
            is_expanded = category_data.get('expanded', True)
            header_text = f"▼{category_name}" if is_expanded else f"▶{category_name}"
            
            category_header = Static(header_text, classes="category-header")
            self.menu_container.mount(category_header)
            self.menu_widgets.append(category_header)
            self.display_items.append({"type": "category", "name": category_name, "widget": category_header})
            total_items += 1
            
            # Add items if expanded
            if is_expanded:
                items = category_data.get('items', [])
                for item in items:
                    item_widget = Static(f"    {item['label']}", classes="menu-item")
                    self.menu_container.mount(item_widget)
                    self.menu_widgets.append(item_widget)
                    self.display_items.append({"type": "item", "data": item, "widget": item_widget})
                    total_items += 1
        
        # Force container refresh and multiple highlighting updates for cross-platform compatibility
        if self.menu_container:
            self.menu_container.refresh()
        
        # Force immediate highlighting update and ensure container shows all content
        self.update_highlighting()
        
        # Ensure container can scroll and shows all content
        if self.menu_container and total_items > 0:
            # Force container to show all content and reset scroll position
            self.menu_container.scroll_home(animate=False)
            # Ensure the current selection is visible
            if 0 <= self.current_index < len(self.display_items):
                try:
                    widget = self.display_items[self.current_index]["widget"]
                    widget.scroll_visible()
                except (IndexError, KeyError):
                    pass
    
    def cleanup_empty_categories(self) -> None:
        """Remove categories that have no items."""
        updated_data = {}
        for category_name, category_data in self.menu_data.items():
            items = category_data.get('items', [])
            if items:  # Only keep categories that have items
                updated_data[category_name] = category_data
        
        if updated_data != self.menu_data:
            self.menu_data = updated_data
            self.save_menu_data()
    
    def update_highlighting(self) -> None:
        """Update visual highlighting with enhanced Linux compatibility."""
        if not self.display_items:
            return

        # Ensure index is always within valid range
        current_idx = max(0, min(self.current_index, len(self.display_items) - 1))
        object.__setattr__(self, 'current_index', current_idx)

        # Clear all selections with explicit widget access and platform-specific timing
        for i, item in enumerate(self.display_items):
            widget = item.get("widget")
            if widget and hasattr(widget, "remove_class"):
                widget.remove_class("-selected")
                # Force immediate refresh for Linux systems
                if hasattr(widget, "refresh"):
                    widget.refresh()
        
        # Apply selection to current item with explicit validation
        if 0 <= current_idx < len(self.display_items):
            current_item = self.display_items[current_idx]
            current_widget = current_item.get("widget")
            
            if current_widget and hasattr(current_widget, "add_class"):
                current_widget.add_class("-selected")
                
                # Force immediate visual update for Linux terminals
                if hasattr(current_widget, "refresh"):
                    current_widget.refresh()
                
                # Enhanced scrolling with Linux-specific optimizations
                if self.menu_container:
                    self.ensure_widget_visible(current_widget, current_idx)
    
    def ensure_widget_visible(self, widget, index: int) -> None:
        """Ensure widget is visible with Linux-optimized scrolling."""
        if not widget or not self.menu_container:
            return
            
        try:
            # Primary scrolling method for most terminals
            if hasattr(widget, "scroll_visible"):
                widget.scroll_visible(animate=False)
                return
        except Exception:
            pass
            
        try:
            # Alternative for containers that support widget scrolling
            if hasattr(self.menu_container, "scroll_to_widget"):
                self.menu_container.scroll_to_widget(widget, animate=False)
                return
        except Exception:
            pass
            
        # Linux-specific fallback with manual calculation
        if self.is_linux_system:
            try:
                # Calculate widget position and container viewport
                widget_region = getattr(widget, 'region', None)
                container_region = getattr(self.menu_container, 'region', None)
                
                if widget_region and container_region:
                    # Simple scroll calculation based on widget position
                    widget_top = widget_region.y
                    container_height = container_region.height
                    
                    # Scroll to ensure widget is in viewport
                    if hasattr(self.menu_container, 'scroll_to'):
                        scroll_y = max(0, widget_top - (container_height // 2))
                        self.menu_container.scroll_to(0, scroll_y, animate=False)
            except Exception:
                # Final fallback: force container refresh
                if hasattr(self.menu_container, 'refresh'):
                    self.menu_container.refresh()
    
    def update_title(self) -> None:
        """Update the header title."""
        if hasattr(self, 'header'):
            self.title = self.app_title
            self.sub_title = ""
    
    def update_status(self) -> None:
        """Update status bar."""
        if self.status_bar:
            total = len(self.display_items)
            current = self.current_index + 1 if self.display_items else 0
            theme_name = self.app_theme.title()
            self.status_bar.update(f"Item {current}/{total} | Theme: {theme_name} | ↑↓ Navigate | Enter Execute | E Edit | I Info | ^B Scan")
    
    def watch_current_index(self, new_index: int) -> None:
        """React to index changes."""
        # Disable reactive updates to prevent conflicts
        pass
    
    def watch_menu_data(self, new_data: Dict[str, Any]) -> None:
        """React to menu data changes."""
        self.update_menu_display()
        self.update_status()
    
    async def action_cursor_up(self) -> None:
        """Move cursor up with enhanced Linux compatibility."""
        if not self.display_items or len(self.display_items) == 0:
            return
        
        # Calculate new index with wrap-around for better UX
        new_index = (self.current_index - 1) % len(self.display_items)
        
        if new_index != self.current_index:
            # Direct assignment without triggering reactive updates
            object.__setattr__(self, 'current_index', new_index)
            
            # Linux-optimized update strategy
            if self.is_linux_system:
                # Immediate synchronous updates for Linux terminals
                self.update_highlighting()
                self.update_status()
            else:
                # Asynchronous updates for other systems
                self.call_after_refresh(self.update_highlighting)
                self.call_after_refresh(self.update_status)
    
    async def action_cursor_down(self) -> None:
        """Move cursor down with enhanced Linux compatibility."""
        if not self.display_items or len(self.display_items) == 0:
            return
        
        # Calculate new index with wrap-around for better UX
        new_index = (self.current_index + 1) % len(self.display_items)
        
        if new_index != self.current_index:
            # Direct assignment without triggering reactive updates
            object.__setattr__(self, 'current_index', new_index)
            
            # Linux-optimized update strategy
            if self.is_linux_system:
                # Immediate synchronous updates for Linux terminals
                self.update_highlighting()
                self.update_status()
            else:
                # Asynchronous updates for other systems
                self.call_after_refresh(self.update_highlighting)
                self.call_after_refresh(self.update_status)
    
    async def action_execute_item(self) -> None:
        """Execute item or toggle category based on selection."""
        if not self.display_items or self.current_index >= len(self.display_items):
            return
        
        current_item = self.display_items[self.current_index]
        
        if current_item["type"] == "item":
            # Execute the application
            command = current_item["data"].get("cmd", "")
            if command:
                pause_setting = current_item["data"].get("pause", False)
                await self.run_external_command(command, pause_setting)
            else:
                pass  # Silently handle missing command
        elif current_item["type"] == "category":
            # Toggle category expansion/collapse
            await self.action_toggle_category()
    
    async def run_external_command(self, command: str, pause: bool = False) -> None:
        """Run external command and return to menu."""
        try:
            with self.suspend():
                os.system('clear')
                print(f"MenuWorks: Executing '{command}'")
                print("=" * 60)
                print()
                
                result = subprocess.run(command, shell=True)
                
                if pause:
                    # Show completion message and wait for keypress
                    print()
                    print("=" * 60)
                    print(f"Command completed with exit code: {result.returncode}")
                    print("Press Enter to return to MenuWorks...")
                    input()
                    os.system('clear')
                else:
                    # Clear screen immediately after app exits
                    os.system('clear')
            
        except Exception as e:
            pass  # Silently handle execution errors
    
    async def action_toggle_category(self) -> None:
        """Toggle category expansion and save state."""
        if not self.display_items or self.current_index >= len(self.display_items):
            return
        
        current_item = self.display_items[self.current_index]
        
        if current_item["type"] == "category":
            category_name = current_item["name"]
            if category_name in self.menu_data:
                # Remember the category we're toggling to restore position
                selected_category = category_name
                
                # Toggle expanded state
                current_state = self.menu_data[category_name].get('expanded', True)
                updated_data = dict(self.menu_data)
                updated_data[category_name]['expanded'] = not current_state
                self.menu_data = updated_data
                
                # Save state to persist across restarts
                self.save_menu_data()
                
                # Update display to reflect changes
                self.update_menu_display()
                
                # Restore position to the same category after display update
                self.restore_position_to_category(selected_category)
    
    def restore_position_to_category(self, category_name: str) -> None:
        """Restore cursor position to the specified category after display update."""
        for i, item in enumerate(self.display_items):
            if item["type"] == "category" and item["name"] == category_name:
                self.current_index = i
                break
    
    def action_show_info(self) -> None:
        """Show info for current item."""
        if not self.display_items or self.current_index >= len(self.display_items):
            return
        
        current_item = self.display_items[self.current_index]
        
        if current_item["type"] == "item":
            self.push_screen(InfoScreen(current_item["data"]))
        else:
            pass  # Silently handle category info requests
    
    def action_edit_item(self) -> None:
        """Edit the currently selected item or category."""
        if not self.display_items or self.current_index >= len(self.display_items):
            return
        
        current_item = self.display_items[self.current_index]
        
        if current_item["type"] == "item":
            categories = list(self.menu_data.keys())
            item_data = current_item["data"]
            
            def handle_edit_result(result):
                if result and result.get("action") == "save":
                    self.update_item(item_data, result["data"])
            
            self.push_screen(EditItemScreen(item_data, categories, self.current_index), callback=handle_edit_result)
        
        elif current_item["type"] == "category":
            category_name = current_item["name"]
            
            def handle_category_edit_result(result):
                if result and result.get("action") == "save":
                    self.rename_category(result["old_name"], result["new_name"])
            
            self.push_screen(EditCategoryScreen(category_name), callback=handle_category_edit_result)
    
    def action_new_item(self) -> None:
        """Create a new menu item."""
        categories = list(self.menu_data.keys())
        if not categories:
            categories = ["General"]
        
        new_item = {"label": "", "cmd": "", "info": "", "category": categories[0]}
        
        def handle_new_result(result):
            if result and result.get("action") == "save":
                self.add_new_item(result["data"])
        
        self.push_screen(EditItemScreen(new_item, categories, -1), callback=handle_new_result)
    
    def add_new_item(self, item_data: Dict[str, str]) -> None:
        """Add a new item to the menu."""
        category = item_data.get('category', 'General')
        
        # Ensure category exists
        updated_data = dict(self.menu_data)
        if category not in updated_data:
            updated_data[category] = {"expanded": True, "items": []}
        
        # Add item to category
        updated_data[category]['items'].append(item_data)
        self.menu_data = updated_data
        self.save_menu_data()
        self.update_menu_display()
    
    def update_item(self, old_item: Dict[str, str], new_item: Dict[str, str]) -> None:
        """Update an existing item."""
        # Find and update the item by matching label and command
        updated_data = dict(self.menu_data)
        
        old_label = old_item.get('label', '')
        old_cmd = old_item.get('cmd', '')
        
        for category_name, category_data in updated_data.items():
            items = category_data.get('items', [])
            for i, item in enumerate(items):
                # Match by label and command to find the right item
                if (item.get('label', '') == old_label and 
                    item.get('cmd', '') == old_cmd):
                    items[i] = new_item
                    self.menu_data = updated_data
                    self.save_menu_data()
                    self.update_menu_display()
                    return
    
    def rename_category(self, old_name: str, new_name: str) -> None:
        """Rename a category and update all items in it."""
        if old_name not in self.menu_data or new_name == old_name:
            return
        
        updated_data = dict(self.menu_data)
        
        # Copy category data to new name
        category_data = updated_data[old_name].copy()
        updated_data[new_name] = category_data
        
        # Update all items to use new category name
        for item in category_data.get('items', []):
            item['category'] = new_name
        
        # Remove old category
        del updated_data[old_name]
        
        self.menu_data = updated_data
        self.save_menu_data()
        self.update_menu_display()
    
    async def action_delete_item(self) -> None:
        """Delete the currently selected item."""
        if not self.display_items or self.current_index >= len(self.display_items):
            return
        
        current_item = self.display_items[self.current_index]
        
        if current_item["type"] == "item":
            item_data = current_item["data"]
            category = item_data.get('category')
            
            # Remove item from category
            updated_data = dict(self.menu_data)
            if category in updated_data:
                items = updated_data[category].get('items', [])
                if item_data in items:
                    items.remove(item_data)
                    
                    # Remove empty category
                    if not items:
                        del updated_data[category]
                    
                    self.menu_data = updated_data
                    self.save_menu_data()
                    self.update_menu_display()
                    
                    # Adjust current index
                    if self.current_index >= len(self.display_items) - 1:
                        self.current_index = max(0, len(self.display_items) - 2)

    def action_change_theme(self) -> None:
        """Open theme selection screen."""
        def handle_theme_result(result):
            if result and result.get("action") == "apply":
                self.app_theme = result["theme"]
                self.apply_theme(result["theme"])
                self.save_menu_data()  # Save theme to persist across sessions
        
        self.push_screen(ThemeSelectionScreen(self.app_theme), callback=handle_theme_result)
    
    def action_edit_title(self) -> None:
        """Open title editing screen."""
        def handle_title_result(result):
            if result and result.get("action") == "save":
                self.app_title = result["title"]
                self.update_title()
                self.save_menu_data()
        
        self.push_screen(EditTitleScreen(self.app_title), callback=handle_title_result)
    
    def apply_theme(self, theme_name: str) -> None:
        """Apply theme colors to the entire application."""
        theme_data = ThemeSelectionScreen.THEMES.get(theme_name, ThemeSelectionScreen.THEMES["classic"])
        
        # Create dynamic CSS with theme colors
        dynamic_css = f"""
        Screen {{
            background: {theme_data['bg']};
        }}
        
        Header {{
            background: {theme_data['primary']};
            color: white;
            text-align: center;
            height: 3;
        }}
        
        Footer {{
            background: {theme_data['primary']};
            color: {theme_data['text']};
            height: 3;
        }}
        
        .main-container {{
            height: 1fr;
            border: solid {theme_data['primary']};
            background: {theme_data['surface']};
            padding: 1;
        }}
        
        .status-bar {{
            dock: top;
            height: 3;
            background: {theme_data['primary']};
            color: {theme_data['text']};
            text-align: center;
            padding: 1;
        }}
        
        .menu-container {{
            height: 1fr;
            border: solid {theme_data['primary']};
            background: {theme_data['surface']};
            padding: 1;
            margin: 1;
            overflow-y: auto;
            min-height: 20;
        }}
        
        .category-header {{
            height: 2;
            padding: 0 1;
            margin: 0;
            background: {theme_data['surface']};
            color: {theme_data['text']};
            text-style: bold;
            border: none;
        }}
        
        .category-header.-selected {{
            background: {theme_data['accent']};
            color: {theme_data['bg']};
        }}
        
        .menu-item {{
            height: 2;
            padding: 0 2;
            margin: 0;
            background: {theme_data['surface']};
            color: {theme_data['text']};
            border: none;
        }}
        
        .menu-item.-selected {{
            background: {theme_data['accent']};
            color: {theme_data['bg']};
            text-style: bold;
        }}
        
        .info-container {{
            align: center middle;
            width: 70;
            height: auto;
            background: {theme_data['surface']};
            border: solid {theme_data['accent']};
            padding: 2;
        }}
        
        .info-title {{
            text-align: center;
            text-style: bold;
            color: {theme_data['accent']};
            margin-bottom: 1;
        }}
        
        .info-field {{
            color: {theme_data['text']};
            margin-bottom: 1;
        }}
        
        .info-description {{
            color: {theme_data['text']};
            text-style: italic;
            margin-bottom: 1;
        }}
        
        .edit-container {{
            align: center middle;
            width: 80;
            height: auto;
            background: {theme_data['surface']};
            border: solid {theme_data['accent']};
            padding: 2;
        }}
        
        .edit-title {{
            text-align: center;
            text-style: bold;
            color: {theme_data['accent']};
            margin-bottom: 1;
        }}
        
        .button-row {{
            align: center middle;
            height: auto;
            margin-top: 1;
        }}
        
        Button {{
            margin: 0 1;
        }}
        """
        
        # Apply the dynamic CSS
        self.stylesheet.add_source(dynamic_css)
    
    def action_scan_bin_directory(self) -> None:
        """Scan ./bin directory and add executables as menu items."""
        self.scan_and_add_bin_executables()
    
    def scan_and_add_bin_executables(self) -> None:
        """Scan ./bin directory for executables and add them to menu."""
        bin_path = Path("./bin")
        
        if not bin_path.exists() or not bin_path.is_dir():
            return  # Silent handling - no bin directory found
        
        # Get existing commands to avoid duplicates
        existing_commands = set()
        for category_data in self.menu_data.values():
            for item in category_data.get('items', []):
                cmd = item.get('cmd', '').strip()
                if cmd:
                    existing_commands.add(cmd)
        
        # Scan for executable files
        new_executables = []
        try:
            for file_path in bin_path.iterdir():
                if file_path.is_file() and os.access(file_path, os.X_OK):
                    # Create command path relative to current directory
                    cmd = f"./bin/{file_path.name}"
                    
                    # Skip if already exists
                    if cmd in existing_commands:
                        continue
                    
                    # Create menu item
                    executable_name = file_path.name.replace('_', ' ').replace('-', ' ').title()
                    new_item = {
                        "label": executable_name,
                        "cmd": cmd,
                        "info": f"Executable: {file_path.name}",
                        "category": "Bin Executables"
                    }
                    new_executables.append(new_item)
        
        except Exception:
            return  # Silent handling of scan errors
        
        # Add new executables to menu
        if new_executables:
            # Ensure "Bin Executables" category exists
            if "Bin Executables" not in self.menu_data:
                updated_data = dict(self.menu_data)
                updated_data["Bin Executables"] = {
                    "expanded": True,
                    "items": []
                }
                self.menu_data = updated_data
            
            # Add new items to the category
            for new_item in new_executables:
                self.add_new_item(new_item)
    
    async def action_exit_app(self) -> None:
        """Exit the application."""
        self.exit()


def main():
    """Main entry point."""
    app = MenuMaker()
    app.run()


if __name__ == "__main__":
    main()
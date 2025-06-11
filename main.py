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
        padding: 1;
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
        margin: 1;
        overflow-y: auto;
        min-height: 20;
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
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("tab", "cursor_down", "Next", show=False),
        Binding("shift+tab", "cursor_up", "Previous", show=False),
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
        self.load_menu_data()
    
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
            self.notify(f"Error saving menu data: {e}", severity="error")
    
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
        for category_name, category_data in self.menu_data.items():
            # Add category header with proper prefix
            is_expanded = category_data.get('expanded', True)
            header_text = f"▼{category_name}" if is_expanded else f"▶{category_name}"
            
            category_header = Static(header_text, classes="category-header")
            self.menu_container.mount(category_header)
            self.menu_widgets.append(category_header)
            self.display_items.append({"type": "category", "name": category_name, "widget": category_header})
            
            # Add items if expanded
            if is_expanded:
                for item in category_data.get('items', []):
                    item_widget = Static(f"  {item['label']}", classes="menu-item")
                    self.menu_container.mount(item_widget)
                    self.menu_widgets.append(item_widget)
                    self.display_items.append({"type": "item", "data": item, "widget": item_widget})
        
        # Update highlighting and ensure container refreshes
        self.update_highlighting()
        
        # Force container refresh to show all items
        if self.menu_container:
            self.menu_container.refresh()
            # Ensure all widgets are visible and force layout
            self.call_later(self.update_highlighting)
    
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
        """Update visual highlighting for current selection."""
        if not self.display_items:
            return

        self.current_index = max(0, min(self.current_index, len(self.display_items) - 1))

        for i, item in enumerate(self.display_items):
            widget = item["widget"]
            if i == self.current_index:
                widget.add_class("-selected")
                if self.menu_container:
                    widget.scroll_visible(animate=False)
            else:
                widget.remove_class("-selected")
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
            self.status_bar.update(f"Item {current}/{total} | Theme: {theme_name} | ↑↓ Navigate | Enter Execute | E Edit | I Info | Space Toggle")
    
    def watch_current_index(self, new_index: int) -> None:
        """React to index changes."""
        if self.display_items:
            self.current_index = max(0, min(new_index, len(self.display_items) - 1))
            self.update_highlighting()
            self.update_status()
        else:
            self.current_index = 0
    
    def watch_menu_data(self, new_data: Dict[str, Any]) -> None:
        """React to menu data changes."""
        self.update_menu_display()
        self.update_status()
    
    async def action_cursor_up(self) -> None:
        """Move cursor up."""
        if self.display_items and len(self.display_items) > 0:
            new_index = max(0, self.current_index - 1)
            if new_index != self.current_index:
                self.current_index = new_index
    
    async def action_cursor_down(self) -> None:
        """Move cursor down."""
        if self.display_items and len(self.display_items) > 0:
            new_index = min(len(self.display_items) - 1, self.current_index + 1)
            if new_index != self.current_index:
                self.current_index = new_index
    
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
                self.notify("No command specified", severity="warning")
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
            
            self.notify(f"Returned from Menu Maker")
            
        except Exception as e:
            self.notify(f"Error executing command: {e}", severity="error")
    
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
            self.notify("No info available for categories", severity="warning")
    
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
        self.notify(f"Added: {item_data['label']}")
    
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
                    self.notify(f"Updated: {new_item['label']}")
                    return
        
        # If not found, notify user
        self.notify(f"Item not found for update: {old_label}", severity="warning")
    
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
        self.notify(f"Renamed category: {old_name} → {new_name}")
    
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
                    self.notify(f"Deleted: {item_data['label']}")
                    
                    # Adjust current index
                    if self.current_index >= len(self.display_items) - 1:
                        self.current_index = max(0, len(self.display_items) - 2)
        else:
            self.notify("Cannot delete categories directly", severity="warning")

    def action_change_theme(self) -> None:
        """Open theme selection screen."""
        def handle_theme_result(result):
            if result and result.get("action") == "apply":
                self.app_theme = result["theme"]
                self.apply_theme(result["theme"])
                self.save_menu_data()  # Save theme to persist across sessions
                self.notify(f"Applied {result['theme'].title()} theme to Menu Maker")
        
        self.push_screen(ThemeSelectionScreen(self.app_theme), callback=handle_theme_result)
    
    def action_edit_title(self) -> None:
        """Open title editing screen."""
        def handle_title_result(result):
            if result and result.get("action") == "save":
                self.app_title = result["title"]
                self.update_title()
                self.save_menu_data()
                self.notify(f"Title updated to: {result['title']}")
        
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
    
    async def action_exit_app(self) -> None:
        """Exit the application."""
        self.exit()


def main():
    """Main entry point."""
    app = MenuMaker()
    app.run()


if __name__ == "__main__":
    main()
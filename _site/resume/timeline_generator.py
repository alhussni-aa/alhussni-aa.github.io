import json
import yaml
import curses
from datetime import datetime

# Path to the JSON file
RESUME_FILE = "resume/resume.json"

# To convert YYYY-MM to MMM YYYY
def convert_date_format(date_str):
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_str, "%Y-%m")
        # Format the date to MMM YYYY
        return date_obj.strftime("%b %Y")
    except ValueError:
        # Handle 'Present' or invalid dates
        if date_str.lower() == "present":
            return "Present"
        return "Invalid date"

# Convert a single entry to YAML format for timeline sections
def convert_entry_to_yaml(entry):
    # Start with the base description
    end_date_org_location = convert_date_format(entry.get("end_date", []))

    # Add unsupported fields to the description
    for field in ["organization", "location"]:
        if field in entry:
            end_date_org_location += f" | {entry[field]}"

    # Return the structured output
    return {
        "title": entry.get("title", "Unknown Title"),
        "from": convert_date_format(entry.get("start_date", "Unknown Start Date")),
        "to": end_date_org_location,
        "description": ", ".join(entry.get("description", "N/A")),
    }

# Convert specific entries to a YAML-compliant flat list
def convert_entries_to_yaml(entries):
    yaml_entries = []
    for entry in entries:
        yaml_entries.append(convert_entry_to_yaml(entry))
    return yaml.dump(yaml_entries, sort_keys=False, allow_unicode=True, default_flow_style=False)

# Load JSON data
def load_resume(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception("Resume JSON file not found.")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON format in the resume file.")

# Save YAML to file
def save_yaml_file(yaml_content, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write(yaml_content)
    except PermissionError:
        raise Exception("Permission denied: Unable to write to the file.")

# Curses-based selection of sections and entries to convert
def curses_interface(stdscr, data):
    curses.curs_set(0)

    # Get the sections in `data` that match `timeline_sections`
    timeline_sections = ["Work Experience", "Leadership Experience", "Education"]
    matching_sections = [
        section for section in data.get("sections", [])
        if section["title"] in timeline_sections
    ]

    selected_entries = []
    section_idx = 0
    entry_idx = 0
    mode = "section"  # Switch between section and entry selection

    while True:
        stdscr.clear()
        if mode == "section":
            stdscr.addstr("Select the sections you want to convert to YAML:\n")
            for idx, section in enumerate(matching_sections):
                if idx == section_idx:
                    stdscr.addstr(f"  > {section['title']}\n", curses.A_REVERSE)
                else:
                    stdscr.addstr(f"  {section['title']}\n")

            stdscr.addstr("\nPress ENTER to select, ARROW KEYS to navigate, 'q' to quit.")

        elif mode == "entry":
            section = matching_sections[section_idx]
            stdscr.addstr(f"Entries in '{section['title']}':\n")
            for idx, entry in enumerate(section["items"]):
                if idx == entry_idx:
                    stdscr.addstr(f"  > {entry.get('title', 'Untitled Entry')}\n", curses.A_REVERSE)
                else:
                    stdscr.addstr(f"  {entry.get('title', 'Untitled Entry')}\n")

            stdscr.addstr("\nPress ENTER to toggle selection, ARROW KEYS to navigate, 'b' to go back.")

        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            if mode == "section":
                section_idx = (section_idx + 1) % len(matching_sections)
            elif mode == "entry":
                entry_idx = (entry_idx + 1) % len(matching_sections[section_idx]["items"])
        elif key == curses.KEY_UP:
            if mode == "section":
                section_idx = (section_idx - 1) % len(matching_sections)
            elif mode == "entry":
                entry_idx = (entry_idx - 1) % len(matching_sections[section_idx]["items"])
        elif key in (curses.KEY_ENTER, 10, 13):
            if mode == "section":
                mode = "entry"
                entry_idx = 0
            elif mode == "entry":
                section = matching_sections[section_idx]
                entry = section["items"][entry_idx]
                if entry not in selected_entries:
                    selected_entries.append(entry)
                else:
                    selected_entries.remove(entry)
        elif key == ord('b') and mode == "entry":
            mode = "section"
        elif key == ord('q'):
            break

    return selected_entries

if __name__ == "__main__":
    output_file = "_data/timeline.yml"

    try:
        # Load the resume data
        resume_data = load_resume(RESUME_FILE)

        # Use curses for user interface
        selected_entries = curses.wrapper(curses_interface, resume_data)

        # Convert the selected entries to YAML
        yaml_content = convert_entries_to_yaml(selected_entries)

        # Save to YAML file
        save_yaml_file(yaml_content, output_file)
        print(f"YAML file has been successfully saved to {output_file}.")

    except Exception as e:
        print(f"Error: {e}")
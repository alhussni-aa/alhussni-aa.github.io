import json
import curses
import re

# Path to the JSON file
RESUME_FILE = "resume/resume.json"

# Sections
SECTIONS = [
    "Education",
    "Work Experience",
    "Leadership Experience",
    "Projects",
    "Awards",
    "Certifications",
    "Publications",
    "Volunteering Opportunities",
    "Languages",
    "Skills",
    "Interests",
    "Extracurriculars",
]

# Load JSON data
def load_resume(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            existing_titles = [section['title'] for section in data.get("sections", [])]
            for section in SECTIONS:
                if section not in existing_titles:
                    data.setdefault("sections", []).append({"title": section, "items": []})
            return data
    except FileNotFoundError:
        return {"sections": [{"title": section, "items": []} for section in SECTIONS]}
    except json.JSONDecodeError:
        return {"sections": [{"title": section, "items": []} for section in SECTIONS]}

# Save JSON data
def save_resume(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except PermissionError:
        raise Exception("Permission denied: Unable to write to the file.")

# Input handler with date validation
def get_input(stdscr, prompt, validate_date=False):
    stdscr.addstr(prompt)
    stdscr.refresh()
    input_str = ""
    while True:
        char = stdscr.getch()
        if char in (curses.KEY_ENTER, 10, 13):  # Enter key
            if validate_date:
                if re.match(r"^\d{4}-(0[1-9]|1[0-2])$", input_str) or input_str.lower() == "present":
                    break
                else:
                    stdscr.addstr("\nInvalid date format. Use YYYY-MM or 'Present'. Try again: ")
                    input_str = ""
            else:
                break
        elif char == 127:  # Backspace key
            if len(input_str) > 0:
                input_str = input_str[:-1]
                y, x = stdscr.getyx()
                stdscr.move(y, x - 1)
                stdscr.addstr(" ")
                stdscr.move(y, x - 1)
        elif 32 <= char <= 126:  # Printable characters
            input_str += chr(char)
            stdscr.addstr(chr(char))
        stdscr.refresh()
    return input_str.strip()

# Create an entry with validation
def create_entry(stdscr, section_title):
    entry = {}
    if section_title in ["Education", "Work Experience", "Leadership Experience"]:
        entry["title"] = get_input(stdscr, "\nEnter the title (e.g., job title, degree): ")
        entry["organization"] = get_input(stdscr, "\nEnter the organization/institution: ")
        entry["location"] = get_input(stdscr, "\nEnter the location: ")
        entry["start_date"] = get_input(stdscr, "\nEnter the start date (YYYY-MM): ", validate_date=True)
        entry["end_date"] = get_input(stdscr, "\nEnter the end date (YYYY-MM or 'Present'): ", validate_date=True)
        entry["description"] = []
        stdscr.addstr("\nEnter bullet points for the description (type 'done' to finish):")
        while True:
            point = get_input(stdscr, "\n- ")
            if point.lower() == "done":
                break
            entry["description"].append(point)
    elif section_title == "Skills":
        entry["name"] = get_input(stdscr, "\nEnter the skill name: ")
        
        # Validate percentage input
        while True:
            percentage = get_input(stdscr, "\nEnter the skill percentage (0-100): ")
            if percentage.isdigit() and 0 <= int(percentage) <= 100:
                entry["percentage"] = int(percentage)
                break
            else:
                stdscr.addstr("\nInvalid input. Please enter a number between 0 and 100.\n")
        
        # Add category with validation
        while True:
            category = get_input(stdscr, "\nEnter the category (Tech/Other): ").strip().lower()
            if category in ["tech", "other"]:
                entry["category"] = category.capitalize()
                break
            else:
                stdscr.addstr("\nInvalid input. Please enter 'Tech' or 'Other'.\n")
    elif section_title == "Languages":
        entry["language"] = get_input(stdscr, "\nEnter the language: ")
        entry["proficiency"] = get_input(stdscr, "\nEnter proficiency (Basic, Fluent, Native): ")
    elif section_title == "Projects":
        entry["name"] = get_input(stdscr, "\nEnter the project name: ")
        entry["tools"] = get_input(stdscr, "\nEnter the tools used (comma-separated): ").split(",")
        entry["image"] = get_input(stdscr, "\nEnter the project image URL: ")
        entry["description"] = get_input(stdscr, "\nEnter the project description: ")
        entry["external_url"] = get_input(stdscr, "\nEnter the external URL (if any): ")
    else:
        entry["title"] = get_input(stdscr, "\nEnter the title: ")
        entry["description"] = []
        stdscr.addstr("\nEnter bullet points for the description (type 'done' to finish):")
        while True:
            point = get_input(stdscr, "\n- ")
            if point.lower() == "done":
                break
            entry["description"].append(point)
    return entry

# Modify an existing entry
def modify_entry(data, section_index, entry_index, stdscr):
    try:
        section = data["sections"][section_index]
        entry = section["items"][entry_index]
        stdscr.addstr(f"\nCurrent entry: {entry}")
        updated_entry = create_entry(stdscr, section["title"])
        section["items"][entry_index] = updated_entry
        stdscr.addstr("\nEntry updated successfully.\n")
    except IndexError:
        stdscr.addstr("\nInvalid section or entry index.\n")

# Delete an entry from a section
def delete_entry(data, section_index, entry_index, stdscr):
    try:
        section = data["sections"][section_index]
        removed_entry = section["items"].pop(entry_index)
        stdscr.addstr(f"\nRemoved entry: {removed_entry}\n")
    except IndexError:
        stdscr.addstr("\nInvalid section or entry index.\n")

# Display all sections with numbers
def list_sections(data, stdscr):
    stdscr.addstr("\nSections:\n")
    for i, section in enumerate(data["sections"]):
        stdscr.addstr(f"  {i + 1}: {section['title']}\n")

# Display entries in a section
def list_entries(data, section_index, stdscr):
    section = data["sections"][section_index]
    stdscr.addstr(f"\nEntries in '{section['title']}':\n")
    for i, item in enumerate(section["items"]):
        stdscr.addstr(f"  {i + 1}: {item}\n")

# Add entry to a section
def add_entry(data, section_index, stdscr):
    section_title = data["sections"][section_index]["title"]
    entry = create_entry(stdscr, section_title)
    data["sections"][section_index]["items"].append(entry)
    stdscr.addstr(f"\nAdded entry to section '{section_title}'.\n")

# Main interactive CLI
def main(stdscr):
    curses.curs_set(1)
    data = load_resume(RESUME_FILE)

    while True:
        stdscr.clear()
        stdscr.addstr("\nResume Management CLI\n")
        stdscr.addstr("1. Add an entry\n")
        stdscr.addstr("2. List entries in a section\n")
        stdscr.addstr("3. Modify an entry\n")
        stdscr.addstr("4. Delete an entry\n")
        stdscr.addstr("5. Exit\n")
        stdscr.addstr("Choose an option: ")
        stdscr.refresh()

        choice = get_input(stdscr, "").strip()

        if choice == "1":
            list_sections(data, stdscr)
            section_index = get_input(stdscr, "Enter the section number to add an entry: ")
            if section_index.isdigit():
                add_entry(data, int(section_index) - 1, stdscr)
            else:
                stdscr.addstr("\nInvalid section number. Please enter a number.\n")

        elif choice == "2":
            list_sections(data, stdscr)
            section_index = get_input(stdscr, "Enter the section number to list entries: ")
            if section_index.isdigit():
                list_entries(data, int(section_index) - 1, stdscr)
            else:
                stdscr.addstr("\nInvalid section number. Please enter a number.\n")

        elif choice == "3":
            list_sections(data, stdscr)
            section_index = get_input(stdscr, "Enter the section number: ")
            if section_index.isdigit():
                section_index = int(section_index) - 1
                list_entries(data, section_index, stdscr)
                entry_index = get_input(stdscr, "Enter the entry number to modify: ")
                if entry_index.isdigit():
                    modify_entry(data, section_index, int(entry_index) - 1, stdscr)
                else:
                    stdscr.addstr("\nInvalid entry number. Please enter a number.\n")
            else:
                stdscr.addstr("\nInvalid section number. Please enter a number.\n")

        elif choice == "4":
            list_sections(data, stdscr)
            section_index = get_input(stdscr, "Enter the section number: ")
            if section_index.isdigit():
                section_index = int(section_index) - 1
                list_entries(data, section_index, stdscr)
                entry_index = get_input(stdscr, "Enter the entry number to delete: ")
                if entry_index.isdigit():
                    delete_entry(data, section_index, int(entry_index) - 1, stdscr)
                else:
                    stdscr.addstr("\nInvalid entry number. Please enter a number.\n")
            else:
                stdscr.addstr("\nInvalid section number. Please enter a number.\n")

        elif choice == "5":
            stdscr.addstr("\nExiting. Goodbye!\n")
            break

        else:
            stdscr.addstr("\nInvalid option. Please try again.\n")

        # Save after every operation
        try:
            save_resume(RESUME_FILE, data)
        except Exception as e:
            stdscr.addstr(f"\nError saving data: {e}\n")
        stdscr.addstr("Press any key to continue...\n")
        stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
import json
import yaml
import curses

# Path to the JSON file
RESUME_FILE = "resume/resume.json"

# Convert a single skill entry to YAML format
def convert_skill_to_yaml(skill):
    return {
        "name": skill.get("name", "Unknown Skill"),
        "percentage": skill.get("percentage", 0),
        "color": skill.get("color", "primary"),  # Default color is 'primary'
        "category": skill.get("category", "Unknown"),
    }

# Convert specific skill entries to a YAML-compliant flat list
def convert_skills_to_yaml(entries):
    yaml_entries = []
    for skill in entries:
        yaml_entries.append(convert_skill_to_yaml(skill))
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

# Input handler for curses
def get_input(stdscr, prompt):
    stdscr.addstr(prompt)
    stdscr.refresh()
    input_str = ""
    while True:
        char = stdscr.getch()
        if char in (curses.KEY_ENTER, 10, 13):  # Enter key
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

# Curses-based selection of skills to convert
def curses_interface(stdscr, data, category):
    curses.curs_set(0)
    skills_section = next((section for section in data.get("sections", []) if section["title"] == "Skills"), None)

    if not skills_section:
        raise Exception("No 'Skills' section found in the resume.")

    selected_skills = []
    skill_idx = 0

    filtered_skills = [skill for skill in skills_section["items"] if skill.get("category", "Unknown").lower() == category.lower()]

    if not filtered_skills:
        raise Exception(f"No skills found in the '{category}' category.")

    while True:
        stdscr.clear()
        stdscr.addstr(f"Select the {category} skills you want to include in the YAML file:\n")
        for idx, skill in enumerate(filtered_skills):
            if idx == skill_idx:
                stdscr.addstr(f"  > {skill.get('name', 'Unnamed Skill')} ({skill.get('percentage', 0)}%) - Color: {skill.get('color', 'primary')}", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {skill.get('name', 'Unnamed Skill')} ({skill.get('percentage', 0)}%) - Color: {skill.get('color', 'primary')}")

        stdscr.addstr("\nPress ENTER to toggle selection, 'c' to assign/edit color, ARROW KEYS to navigate, 'q' to quit.")

        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            skill_idx = (skill_idx + 1) % len(filtered_skills)
        elif key == curses.KEY_UP:
            skill_idx = (skill_idx - 1) % len(filtered_skills)
        elif key in (curses.KEY_ENTER, 10, 13):
            skill = filtered_skills[skill_idx]
            if skill not in selected_skills:
                selected_skills.append(skill)
            else:
                selected_skills.remove(skill)
        elif key == ord('c'):
            skill = filtered_skills[skill_idx]
            assign_color_to_skill(stdscr, skill)
        elif key == ord('q'):
            break

    return selected_skills

# Function to prompt color selection during entry creation in curses
def assign_color_to_skill(stdscr, skill):
    valid_colors = ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]
    stdscr.clear()
    stdscr.addstr(f"Assign a color to the skill '{skill['name']}' (options: {', '.join(valid_colors)}):\n")
    stdscr.refresh()

    while True:
        color = get_input(stdscr, "Enter color: ").strip().lower()
        if color in valid_colors:
            skill["color"] = color
            break
        else:
            stdscr.addstr(f"\nInvalid color. Please choose from: {', '.join(valid_colors)}\n")

if __name__ == "__main__":
    tech_output_file = "_data/tech-skills.yml"
    other_output_file = "_data/other-skills.yml"

    try:
        # Load the resume data
        resume_data = load_resume(RESUME_FILE)

        # Use curses for Tech skills
        tech_skills = curses.wrapper(curses_interface, resume_data, "Tech")
        tech_yaml_content = convert_skills_to_yaml(tech_skills)
        save_yaml_file(tech_yaml_content, tech_output_file)
        print(f"Tech skills YAML file has been successfully saved to {tech_output_file}.")

        # Use curses for Non-Tech skills
        other_skills = curses.wrapper(curses_interface, resume_data, "Other")
        other_yaml_content = convert_skills_to_yaml(other_skills)
        save_yaml_file(other_yaml_content, other_output_file)
        print(f"Other skills YAML file has been successfully saved to {other_output_file}.")

    except Exception as e:
        print(f"Error: {e}")
import json
import yaml
import curses
import os

# Path to the JSON file
RESUME_FILE = "resume/resume.json"
PROJECTS_DIR = "_projects"

# Ensure the projects directory exists
os.makedirs(PROJECTS_DIR, exist_ok=True)

# Convert a single project to Markdown format
def convert_project_to_md(project):
    md_content = f"""---
name: {project.get('name', 'Unnamed Project')}
tools: {project.get('tools', [])}
image: {project.get('image', '')}
description: {project.get('description', 'No description provided.')}
external_url: {project.get('external_url', '')}
---"""
    return md_content

# Save a project to an individual Markdown file
def save_project_md_file(project, output_dir):
    file_name = f"{project.get('name', 'Unnamed_Project').replace(' ', '_').lower()}.md"
    file_path = os.path.join(output_dir, file_name)
    try:
        with open(file_path, 'w') as file:
            file.write(convert_project_to_md(project))
        print(f"Project saved to {file_path}")
    except PermissionError:
        raise Exception(f"Permission denied: Unable to write to {file_path}")

# Load JSON data
def load_resume(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception("Resume JSON file not found.")
    except json.JSONDecodeError:
        raise Exception("Invalid JSON format in the resume file.")

# Curses-based project selection interface
def curses_project_interface(stdscr, data):
    curses.curs_set(0)
    projects_section = next((section for section in data.get("sections", []) if section["title"] == "Projects"), None)

    if not projects_section:
        raise Exception("No 'Projects' section found in the resume.")

    selected_projects = []
    project_idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr("Select the projects you want to export to Markdown files:\n")
        for idx, project in enumerate(projects_section["items"]):
            if idx == project_idx:
                stdscr.addstr(f"  > {project.get('name', 'Unnamed Project')}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {project.get('name', 'Unnamed Project')}\n")

        stdscr.addstr("\nPress ENTER to toggle selection, ARROW KEYS to navigate, 'q' to quit.")

        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            project_idx = (project_idx + 1) % len(projects_section["items"])
        elif key == curses.KEY_UP:
            project_idx = (project_idx - 1) % len(projects_section["items"])
        elif key in (curses.KEY_ENTER, 10, 13):
            project = projects_section["items"][project_idx]
            if project not in selected_projects:
                selected_projects.append(project)
            else:
                selected_projects.remove(project)
        elif key == ord('q'):
            break

    return selected_projects

if __name__ == "__main__":
    try:
        # Load the resume data
        resume_data = load_resume(RESUME_FILE)

        # Use curses for project selection
        selected_projects = curses.wrapper(curses_project_interface, resume_data)

        # Save each selected project to a Markdown file
        for project in selected_projects:
            save_project_md_file(project, PROJECTS_DIR)

    except Exception as e:
        print(f"Error: {e}")
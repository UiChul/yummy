import os
import json

def find_server_path(self):
        """Finds the matching folder and updates the UI."""

        json_file_path = 'C:/home/rapa/YUMMY/pipeline/json/projcet_data.json'
        path_finder = PathFinder(json_file_path)

        start_path = ' C:/home/rapa/YUMMY/project'
        
        # Get the new path
        new_path = path_finder.append_project_to_path(start_path)
        
        if new_path:
            print(f"New path with project appended: {new_path}")
        else:
            print("Failed to generate new path.")

        self.find_server_path()
# if __name__ == "__main__":

class PathFinder:

    def __init__(self, json_file_path, key):
        self.json_file_path = json_file_path
        self.key = 'project'
        self.json_data = self._read_paths_from_json()

    def _read_paths_from_json(self):
        """Reads the JSON file and returns the data."""
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: The file {self.json_file_path} was not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: The JSON file could not be decoded.")
            return {}

    def append_project_to_path(self, start_path):
        """Finds the folder in the JSON data that matches the basename of start_path."""
        # Check if the specified key exists in the JSON data
        if self.key not in self.json_data:
            print(f"Error: Key '{self.key}' not found in the JSON data.")
            return None

        # Get the project value
        project_value = self.json_data[self.key]
        
        # Ensure start_path does not end with a separator
        start_path = start_path.rstrip(os.sep)
        
        # Append the project value to the start_path
        new_path = os.path.join(start_path, project_value)
        
        return new_path
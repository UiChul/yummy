# import ffmpeg
import os
import json

class PathFinder:
    """
    Read Json File and find matching material (key:project_name)
    and then find Local path
    """

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.key = 'project'
        self.json_data = self._read_paths_from_json()

    def _read_paths_from_json(self):
        """Read Json file and data return"""
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    def append_project_to_path(self, start_path):
        """Find data that matches key(project_name) in Json data"""
        project_value = self.json_data[self.key]
        start_path = start_path.rstrip(os.sep)
        new_path = f"{start_path}/{project_value}/"
        return new_path
    
    def data_needed(self):
        data_json = self._read_paths_from_json() 
        project_name= data_json[self.key]
        project_id = data_json['id']
        user_name = data_json['name']
        project_res_width = data_json['resolution_width']
        project_res_height = data_json['resolution_height']
        list_needed = [project_name, project_id, user_name, project_res_width, project_res_height]
        return list_needed
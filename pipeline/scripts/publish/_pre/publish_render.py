
import os
import nuke
from publish_module import Slate
from publish_module2 import PathFinder

class Render:
    def __init__(self):
        super().__init__()

        self.find_write_node()

    def find_write_node(self):
        select_nodes = nuke.selectedNodes()
        if not select_nodes:
            print("선택된 write노드가 없습니다.")
            return
        
        for node in select_nodes:
            if node.Class() == "Write":
                self.write_node = node
                if self.write_node.inputs() == 0:
                    nuke.message("write노드를 렌더링할 노드에 연결해주세요.")
                else:
                    self.start_render()
                    nuke.message("렌더링이 완료되었습니다.")

            else:
                nuke.message("write노드를 선택해주세요.")
    
    def start_render(self):
        self.render_exr()
        self.render_mov()

    def render_exr(self):
        exr_path = self.set_the_file_path()[0]
        exr_folder_path = os.path.dirname(exr_path)

        self.write_node["file"].setValue(exr_path)
        self.write_node["file_type"].setValue("exr")

        if os.path.isdir(exr_folder_path):
            nuke.execute(self.write_node)
            # self.put_the_slate_in_file()
        else:
            os.makedirs(exr_folder_path)
            nuke.execute(self.write_node)
            # self.put_the_slate_in_file()

    def render_mov(self):
        
        mov_path = self.set_the_file_path()[1]

        self.write_node["file"].setValue(mov_path)
        self.write_node["file_type"].setValue("mov")
        self.write_node["codec"].setValue("ProRes")

        # render = Slate()
        # render.start_exr(exr_path,exr_output)

        nuke.execute(self.write_node)

    def set_the_file_path(self):

        json_file_path = 'C:/home/rapa/YUMMY/pipeline/json/project_data.json'
        path_finder = PathFinder(json_file_path)

        start_path = '/home/rapa/YUMMY/project'

        project_path = path_finder.append_project_to_path(start_path)
        seq_path = f"{project_path}seq/"

        nuke_path = nuke.scriptName()
        nuke_file_name = os.path.basename(nuke_path)
        base, _ = os.path.splitext(nuke_file_name)
        item = nuke_file_name.split("_")
        shot = item[0]
        code = item[1]
        team_name = item[2]
        # ver_numb = item[3].split(".")[0]
        
        a = "%4d"
        exr_file_path = f"{seq_path}{shot}/{shot}_{code}/{team_name}/dev/exr/{base}/{base}.{a}.exr"
        mov_file_path = f"{seq_path}{shot}/{shot}_{code}/{team_name}/dev/mov/{base}.mov"

        print(f"{exr_file_path}: 이엑ㄱ스알")
        print(f"{mov_file_path}: 이엑ㄱ스알")
        return exr_file_path, mov_file_path
    
    # def put_the_slate_in_file(self):
    #     exr_path, mov_path = self.set_the_file_path()
    #     exr_dir = os.path.dirname(exr_path)
    #     print(f"{exr_dir}: 디렉토리")
    #     render = Slate()
    #     render.start_exr(exr_dir, mov_path)


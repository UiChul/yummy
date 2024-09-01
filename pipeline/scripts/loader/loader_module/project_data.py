# 이건 결국 프로젝트 들어가서 확인을 해야하는 부분이니까 
# 로그인 창에서 프로젝트를 넣어서 들어가면
# 일단 ui에 들어가게 되니까 이걸 사용하면 될 거 같다??
# file_info에 resolution도 같이 넣어주면 될 거 같다??

# from pipeline.scripts.loader.loader_ui.main_window_v002_ui import Ui_Form
import json

class project_data:
    def __init__(self,info):
        
        self.resolution = ""
        
        self.open_json()
        
        info["resolution"] = self.resolution
        return info
     
    def open_json(self):
        with open("/home/rapa/yummy/pipeline/json/login_user_data.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
            
        self.find_project_resolution(user_dic)
            
    def find_project_resolution(self,project_info):
        project_name = self.ui.label_projectname.text()
        print(project_name)
        
        for project in project_info["projects"]:
            if project["name"] == project_name:
                width = project["resolution_width"]
                height = project["resolution_height"]
                
                self.resolution = f"{width} X {height}"
                     
                
                
                
                
                
        
        
            
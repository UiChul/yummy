print ("*" * 30)
print ("menu.py")
print ("메뉴 스크립트가 실행됨")
print ("*" * 30)


import nuke
import pipeline_script

#누크안에 풀다운 메뉴 만들기
menu_bar = nuke.menu("Upload")
menu_4th = menu_bar.addMenu("Shotgrid upload")

# addCommand(라벨(메뉴이름), 명령, 바로가기, 순서)  ++바로가기와 순서는 없어도 실행이 되긴함
menu_4th.addCommand("hello world", pipeline_script.test_func, "F8")
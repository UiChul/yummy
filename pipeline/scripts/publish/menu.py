print ("*" * 30)
print ("menu.py")
print ("메뉴 스크립트가 실행됨")
print ("*" * 30)


import nuke
import publish_0901_for_lu

#누크안에 풀다운 메뉴 만들기
menu_bar = nuke.menu("Nuke")
menu_add = menu_bar.addMenu("Upload")

menu_add.addCommand("Shotgrid_upload", publish_0901_for_lu.open_ui_in_nuke, "F8")
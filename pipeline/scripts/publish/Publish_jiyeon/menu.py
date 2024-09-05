print ("*" * 30)
print ("menu.py")
print ("메뉴 스크립트가 실행됨")
print ("*" * 30)


import nuke
import publish_main
import publish_render

#누크안에 풀다운 메뉴 만들기
menu_bar = nuke.menu("Nuke")
menu_add = menu_bar.addMenu("Upload")

menu_add.addCommand("Render", publish_render.start_render_in_nuke, "F7")
menu_add.addCommand("Shotgrid_upload", publish_main.open_ui_in_nuke, "F8")
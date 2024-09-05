print("*" *30)
print("init.py")
print("이니셜라이즈 스크립트가 실행됨")
print("*" *30)

import nuke

nuke.pluginAddPath("./gizmos")
nuke.pluginAddPath("./icons")
nuke.pluginAddPath("./lib")
nuke.pluginAddPath("./lut")
nuke.pluginAddPath("./plugins")
nuke.pluginAddPath("./python")
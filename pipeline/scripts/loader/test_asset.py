import nuke

file_path = "/home/rapa/YUMMY/project/Marvelous/asset/Prop/rig/pub/turntable/cache/turntable.abc"

read_geo_node =  nuke.createNode('ReadGed')
read_geo_node['file'].setValue(file_path)
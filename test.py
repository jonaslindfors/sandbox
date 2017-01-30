import sgtk
import sys
import tank
import ast

def shotgunInfo(context):
    current_engine = sgtk.platform.current_engine()

    context = current_engine.context

    sys.path.append(r"Y:\CHIMNEY_CONFIG\chimney-api")


    from chm_shotgun.ShotgunTankAccess import ShotgunTankAccess
    shotgun_access_obj = ShotgunTankAccess.Shotgun_Tank_Access()
    sg = shotgun_access_obj.get_sg()

    from chm_shotgun.ShotgunTankAccess import CustomQuery
    reload(CustomQuery)
    custom_query_obj = CustomQuery.Custom_Query()

    from chm_shotgun.TimeCodeFetcher import TimeCodeFetcher
    reload(TimeCodeFetcher)
    time_code_fetcher = TimeCodeFetcher.TimeCodeFetcher()

    ctx = context

    # Query the Duration of the Shot
    sg_entity_type = ctx.entity['type']
    sg_entity_id = ctx.entity['id']
    firstFrame = time_code_fetcher.get_cutIn_by_id(sg_entity_id, sg_entity_type)
    lastFrame = time_code_fetcher.get_cutOut_by_id(sg_entity_id, sg_entity_type)

    sg_project_id = ctx.project['id']
    query_result_dict = custom_query_obj.get_project_meta_data_by_id(sg_project_id)

    query_result_dict.update({'first_frame' : firstFrame, 'last_frame' : lastFrame})

    return query_result_dict

current_engine = sgtk.platform.current_engine()
context = current_engine.context

formatTextFile = "Y:/CHIMNEY_CONFIG/nuke/projects/%s/nuke_python/shotgunFormats.txt" % office
openFormat = open(formatTextFile, 'r')
formatDic = ast.literal_eval(openFormat.read())

#Get shotgun info
showInfo = shotgunInfo(context)
from flask import Flask, request
from flask_restful import Resource, Api
from pythoncom import CoInitialize
import sys
from os import devnull
from dataHandlers.presetManager import PresetManager as pmgr
from dataHandlers.presetManager import PRESET_LIST_FILE_NAME

app = Flask(__name__)
api = Api(app)

todos = {}

class PresetEndpoints(Resource):
    def get(self, presetId):
        presetList = pmgr.get_all_entries()

        for actPres in presetList:
            if actPres.id == (str(presetId)):
                return actPres.to_Dict()
            
        return "ERROR: No preset with id '" + str(presetId) + "'."
            
    def delete(self, presetId):
        return pmgr.delete_preset(presetId)
    
    def patch(self, presetId):
        data = request.get_json()
        # CoInitialize()
        return pmgr.change_preset(presetId, data['name'], data['description'], data['files'])

class PresetListEndpoints(Resource):
    def get(self):
        presetList = pmgr.get_all_entries()
        presets = []
        for actPres in presetList:
            presets.append(actPres.to_Dict())
        return presets
    
    def post(self):
        data = request.get_json()
        response = pmgr.create_preset(data['name'], data['description'])
        return response
    
class PresetLoadEndpoint(Resource):
    def get(self, presetId):
        presetList = pmgr.get_all_entries()

        for actPres in presetList:
            if str(actPres.id) == (str(presetId)):
                pmgr.load_preset(actPres.name)
                return "Preset '" + actPres.name + "' loaded."
            
        return "ERROR: No preset with id '" + str(presetId) + "'."
    
class PresetSaveEndpoint(Resource):
    def get(self, presetId):
        presetList = pmgr.get_all_entries()

        for actPres in presetList:
            if str(actPres.id) == (str(presetId)):
                pmgr.save_preset(actPres.name)
                return "Preset '" + actPres.name + "' loaded."
            
        return "ERROR: No preset with id '" + str(presetId) + "'."
    
class PresetImportEndpoint(Resource):
    def post(self):
        data = request.get_json()
        # TODO: Handle case when no parameter is getting passed
        # TODO: Require non-empty stirng at Fronend, Backend and here (as the TODO above says)
        # response = pmgr.import_preset(data['source'], data['destination'], data['name'])
        response = pmgr.import_preset(data['source'], PRESET_LIST_FILE_NAME, data['name'])
        return response
    
class PresetExportEndpoint(Resource):
    def post(self):
        data = request.get_json()
        # TODO: Handle case when no parameter is getting passed
        # TODO: Require non-empty stirng at Fronend, Backend and here (as the TODO above says)
        response = pmgr.export_preset(data['name'])
        return response

api.add_resource(PresetEndpoints, '/id/<int:presetId>')
api.add_resource(PresetListEndpoints, '/')
api.add_resource(PresetLoadEndpoint, '/load/<int:presetId>')
api.add_resource(PresetSaveEndpoint, '/save/<int:presetId>')
api.add_resource(PresetImportEndpoint, '/import')
api.add_resource(PresetExportEndpoint, '/export')

if __name__ == '__main__':
    # Silence stdout and stderr (the app is built in no console mode, which then leads to errors when trying to print to stdout/stderr)
    sys.stdout = sys.stderr = open(devnull, 'w')
    app.run(debug=False)
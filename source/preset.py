import json

class Preset:
    def __init__(self, name:str, description:str, registryLocation:str, files:list):
        self.name = name
        self.description = description
        self.registryLocation = registryLocation
        self.files = files

    def to_Json(self):
        '''
        Returns the object as a json string
        '''
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_Dict(self):
        '''
        Returns the object as a dictionary
        '''
        return {"name": self.name, "description": self.description, "registryLocation": self.registryLocation, "files": self.files}
    
    def to_Preset(dict:dict):
        """
        returns a Preset object with the name,description and registryLocation values
        """
        return Preset(dict['name'],dict['description'],dict['registryLocation'],dict['files'])
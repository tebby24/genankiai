import json


class Generator:
    def __init__(self, template_json):
        self.template_json = template_json

    def get_template_info(self):
        with open(self.template_json, "r") as f:
            return json.load(f)

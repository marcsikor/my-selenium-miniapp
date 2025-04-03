from scraper import Scraper

import json

sc = Scraper(False)

with open('credentials.json') as cred:
    credentials_dict = json.load(cred)

with open('portal-paths.json') as paths:
    paths_dict = json.load(paths)

sc.execute_login(credentials_dict["login"], credentials_dict["password"], paths_dict["login-page"])

output = sc.get_grades(paths_dict["grades-page"])

print(json.dumps(output))
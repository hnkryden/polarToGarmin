import os
from pathlib import Path
from requests import Session
import re
import getpass

class PolarFlowClient(Session):
    def __init__(self):
        super().__init__()
    def login(self, username, password):
        return self.post('https://flow.polar.com/login',
                         data={"email": username,
                               "password": password,
                               "returnUrl": '/'})
    def getActivities(self,start='01.11.1990',stop='31.12.2098'):
        activities = self.get('https://flow.polar.com/training/getCalendarEvents',
                      params={'start': start,
                              'end': stop}).json()
        return activities
    def exportToGarmin(self,resultdir):
        activities = self.getActivities()
        if not os.path.exists(resultdir):
            os.makedirs(resultdir)
        for activity in activities:
            if 'listItemId' in activity:
                listItemId = str(activity['listItemId'])
                tcx_export = self.get(
                    'https://flow.polar.com/api/export/training/tcx/' + listItemId
                    )
                tcx_content = tcx_export.content.decode("utf-8")
                tcx_content = re.sub(r'<Creator.*Creator>', '', tcx_content)
                tcx_content = re.sub(r'<Author.*Author>', '', tcx_content)
                filename = listItemId +".tcx"
                file_to_write = resultdir / filename
                f = open(file_to_write, "w");f.write(tcx_content)
                f.close()
                print("Exported %s" % filename)

if __name__ == "__main__":
    flow = PolarFlowClient()
    username = input("Polar username: ")
    pswd = getpass.getpass('Password:')
    status = flow.login(username,pswd) 
    if status.status_code==200:
        resultdir = Path("exported")
        print("Login success, writing results to folder = %s" % str(resultdir))
        flow.exportToGarmin(resultdir)
    else:
        print("Login failed")


#step 1
import json
from datetime import datetime
#2 Read json from products.json to the variable data
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# create varaible report to add report 
report = "datetime.now()"

beautify_it = "=" * 70

comp_name = data["company"]
now = datetime.now()
report_taken_date = now.strftime("%Y-%m-%d %H:%M:%S")
last_updated = data["last_updated"]
report +=  beautify_it + "\n" + (" " * int(len(beautify_it)/3)) + comp_name + "\n" + beautify_it
report += "\n" + "Report generate time : " + str(report_taken_date) 
report += "\n" +"report last updated time :  " + last_updated 

print (report)

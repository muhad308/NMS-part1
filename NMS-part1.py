#step 1
import json
from datetime import datetime
#2 Read json from products.json to the variable data
data = json.load(open("network_devices.json","r",encoding = "utf-8"))
# create varaible report to add report
report = ""
beautify_it = "=" * 70
comp_name = data["company"]
now = datetime.now()
report_taken_date = now.strftime("%Y-%m-%d %H:%M:%S")
last_updated = data["last_updated"]
report +=  beautify_it + "\n" + (" " * int(len(beautify_it)/3)) + comp_name + "\n" + beautify_it
report += "\n" + "Report generate time : " + str(report_taken_date)
report += "\n" +"report last updated time :  " + last_updated
 
report += "\n\n" + ( " " * 20)  + " Exective summary" + "\n" + beautify_it + "\n"
 
# loop through the location list 
offline ="status : OFFLINE \n"
switch ="status : SWITCH \n"
offline_status = 0
warning_status = 0
switches = 0;
router = 0
load_balancer = 0 
firewall = 0
low_up_time_devices = 0
accesspoint = 0
for location in data["locations"]:
    for device in location["devices"]:
        if(device["status"] == "offline"):
            offline_status += 1
            offline += device["hostname"] + "   " + device["ip_address"] + "  " + location["site"] + "\n"
        if(device["status"] == "warning"):
            warning_status +=1
            switch += device["hostname"] + "   " + device["ip_address"] + "  " + location["site"] + "\n"
        if(device["type"] == "switch"):
            switches += 1
        if(device["type"] == "router"):
            router += 1
        if(device["type"] == "access_point"):
            accesspoint += 1
        if(device["type"] == "firewall"):
            firewall += 1
        if(device["type"] == "load_balancer"):
            load_balancer += 1
        if(device["uptime_days"] < 30):
          low_up_time_devices += 1

 
        
 
report += "⚠️  critical :" + str(offline_status) + "\n" 
report += "⚠️  warning  :" + str(warning_status) + "\n"
report += "⚠️  " + str(low_up_time_devices) + " devices with low uptime (<30 days) - may indicate instability"
report += "\n" + offline + "\n"
report += switch  + "\n"
print (report)
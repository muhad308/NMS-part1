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

warning ="status : WARNING \n"

offline_status = 0

warning_status = 0

total_switches = 0

offline_switches = 0

total_routers = 0

offline_routers = 0

total_access_point = 0

offline_access_points = 0

total_firewall = 0

offline_firewall = 0

total_load_balancer = 0

offline_load_balancer = 0

total_number_of_devices = 0

total_offline_devices = 0

low_up_time_devices = 0

low_up_time_info = ""

# collect of ports used and total_number_of_devices

# Header

total_and_used_ports = (

    "\n\n PORT USE SWITCHES \n"

    "------------------------------------------------------------\n"

    f"{'SITE':<15}{'SWITCHES':<15}{'USED/TOTAL':<20}{'USAGE IN PERCENT':<10}\n"

    "------------------------------------------------------------\n"

)

# all ports for all site total and used

all_ports_for_switches = 0

all_used_ports_for_switches = 0

ports_high_usage_table = (

    "\n\n SWITCHES WITH HIGH PORT UTILIZATION (>80%)\n"

    "------------------------------------------------------------\n")

# high utilization ports

count_ports_with_high_utilization = 0
 
# vLan overview table 

vlan_overview_table = (

    "\n\n OVERVIEW \n"

    "------------------------------------------------------------\n")

# get statics per site 

statics_per_site_table = (

    "\n\n STATICS PER SITE \n"

    "------------------------------------------------------------\n")

# as we need uniqu values so set will not take dublicate 

collect_unique_vlan = set();

for location in data["locations"]:

    site_name = location["site"]

    city = location["city"]

    contact_person = location["contact"]

    # total and used ports for switches only per site

    total_ports_per_site = 0

    used_ports_per_site = 0

    switch_for_ports = 0

    # get offline and warning devices persite

    total_online_offline_warning_devices = 0

    total_online_persite = 0

    for device in location["devices"]:

        if(device["status"] == "online"):

            total_online_persite += 1

        if(device["status"] == "offline"):

            offline_status += 1

            offline += device["hostname"] + "   " + device["ip_address"] + "  " + location["site"] + "\n"

        if(device["status"] == "warning"):

            warning_status +=1

            warning += device["hostname"] + "   " + device["ip_address"] + "  " + location["site"] + "\n"

        if(device["type"] == "switch"):

            total_switches += 1

            switch_for_ports += 1

            if "ports" in device:

                total_ports_per_site += device["ports"]["total"]

                used_ports_per_site  += device["ports"]["used"]

            if(device["status"] == "offline"):

                offline_switches += 1

        if(device["type"] == "router"):

            total_routers += 1

            if(device["status"] == "offline"):

                offline_routers += 1

        if(device["type"] == "access_point"):

            total_access_point += 1

            if(device["status"] == "offline"):

                offline_access_points += 1

        if(device["type"] == "firewall"):

            total_firewall += 1

            if(device["status"] == "offline"):

                offline_firewall += 1

        if(device["type"] == "load_balancer"):

            total_load_balancer += 1

            if(device["status"] == "offline"):

                offline_load_balancer += 1

        if(device["uptime_days"] < 30):

          low_up_time_devices += 1

          critical = ""

          critical = ("⚠️ critical" if device["uptime_days"] <= 2 else location["site"])

          low_up_time_info += device["hostname"] + "     " + str(device["uptime_days"]) + "days  " + critical + "\n"

        # get unique vlans

        vlans = device.get("vlans", [])

        collect_unique_vlan.update(vlans)

        # total number of all devices

        total_number_of_devices = total_switches + total_routers + total_access_point + total_firewall + total_load_balancer

        #total number of all offline devices 

        total_offline_devices = offline_switches + offline_routers + offline_access_points + offline_firewall + offline_load_balancer

        # take percentage of offline devices

        total_offline_in_percent = (total_offline_devices / total_number_of_devices) * 100

        total_online_offline_warning_devices = total_online_persite + offline_status + warning_status

    #port usage in percentage

    percent_port = (used_ports_per_site/ total_ports_per_site)*100

    alert_singe = "" if percent_port < 80 else ("⚠️ " if percent_port < 90 else "⚠️ critical")

    if percent_port >= 80:

        alert_ = "⚠️ FULL" if percent_port == 100 else "⚠️ "

        count_ports_with_high_utilization += 1 

        # ports with high usage table 

        ports_high_usage_table += "\n" + device["hostname"] + "     " + "     " +str(used_ports_per_site) + "/" + str(total_ports_per_site) + "    " + str(round(percent_port, 1))+"% " + alert_ +"\n" 

    #create string of ports

    total_and_used_ports += f"{site_name:<15}{switch_for_ports}st{'':<15}{used_ports_per_site}/{total_ports_per_site:<10}{percent_port:<5.2f}%{alert_singe}\n"

    # get all ports and used ports

    all_ports_for_switches += total_ports_per_site

    all_used_ports_for_switches += used_ports_per_site

    # Statics persite table updatation

    statics_per_site_table += (site_name + "(" + city + "): \n   Units :" +

        str(total_online_offline_warning_devices) +"(" + str(total_online_persite) + " online, " +

        str(offline_status) + " offline, " + str(warning_status) + " warning)\n   contact :" + contact_person + "\n\n") 

#get percentage usage of ports for all sites

total_ports_usage_in_percent = (all_used_ports_for_switches / all_ports_for_switches) * 100

# add format to above value as string

total_ports_usage_in_percent = round(total_ports_usage_in_percent, 1)

# as it is a list or set so we would like to have each element separted by comma

number_vlans = str(len(collect_unique_vlan))

collect_unique_vlan = ",".join(str(vlan) for vlan in sorted(collect_unique_vlan))

vlan_overview_table += "\nTotal number of unique VLANs in the network: " + number_vlans +"\n VLANs: " + str(collect_unique_vlan)
 


report += "\n⚠️  critical :" + str(offline_status) + "\n" 

report += "⚠️  warning  :" + str(warning_status) + "\n"

report += "⚠️  " + str(low_up_time_devices) + " devices with low uptime (<30 days) - may indicate instability\n"

report += "⚠️  " + str(count_ports_with_high_utilization) + " switches have high port utilization (>80%)\n"

report += "\n\n         Devices with problem \n------------------------------"

report += "\n\n" + offline + "\n"

report += warning  + "\n\n"

report += "  DEVICES WITH LOW UPTIME (<30 days) \n -------------------------------------\n"

report += low_up_time_info

report += "\n STATISTICS BY DEVICE TYPE \n -------------------------------------"

report += "\n Switch          " + str(total_switches) + "st     " + "(" + str(offline_switches) + " offline)"

report += "\n Routers         " + str(total_routers) +  " st     " + "(" + str(offline_routers) + " offline)"

report += "\n access_points   " + str(total_access_point) +" st     " + "(" + str(offline_access_points) + " offline)"

report += "\n firewalls       " + str(total_firewall) + " st     " + "(" + str(offline_firewall) + " offline)"

report += "\n load_balancer   " + str(total_load_balancer) + " st     " + "(" + str(offline_load_balancer) + " offline)"

report += "\n -------------------------------------\n TOTAL:      " + str(total_number_of_devices)+" units  " + "(" + str(total_offline_devices) + " offline = " + str(total_offline_in_percent)+"% offline)"

#add ports table to report

report += total_and_used_ports

report += "------------------------------------------------------------\n Totalt:      " + str(all_used_ports_for_switches) + "/" + str(all_ports_for_switches) + " ports used             (" +  str(total_ports_usage_in_percent)+"%)"

report += ports_high_usage_table

report += vlan_overview_table

report += statics_per_site_table

print (report)
 
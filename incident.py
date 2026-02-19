import json
import os
import time

def createIncident():
    if not os.path.exists("incidents.json") or os.stat("incidents.json").st_size == 0:
        data = []
        last_id = 0
    else:
        with open("incidents.json", "r") as file:
            data = json.load(file)
        last_id = max([rec["incident_id"] for rec in data], default=0)

    default_status = "open"
    service_name = input("Enter the service name: ")
    severity = input("Enter the severity level(SEV 1/SEV 2/SEV 3): ").upper()
    description = input("Enter Description: ")
    # status = input("Enter the status of your incident(Open/Close): ")
    timestamp_sec = time.ctime()
    print("Timestamp is: ",timestamp_sec)
    new_record = {
        "incident_id": last_id+1,
        "service_name": service_name,
        "severity": severity,
        "description": description,
        "status": default_status,
        "timestamp": timestamp_sec
    }
    if not os.path.exists("incidents.json") or os.stat("incidents.json").st_size == 0:
        data = []
    else:
        with open("incidents.json", "r") as file:
            data = json.load(file)
    data.append(new_record)
    with open("incidents.json", "w") as file:
         json.dump(data, file, indent=4)

def readIncident():
    if not os.path.exists("incidents.json") or os.stat("incidents.json").st_size == 0:
        print("No incidents found.")
        return
    # Viewing all incidents
    with open("incidents.json", "r") as file:
            data = json.load(file)
    print("All incidents: ")
    print(json.dumps(data, indent=4))

    # FIltering the data
    user_ch = input("Do you want to filter it by Severity/Status: ")
    if user_ch.lower() == 'severity':
        sev_in = input("Enter the category in severity(SEV 1/SEV 2/SEV 3): ").upper()
        for rec in data:
            if sev_in in rec.values():
                print(json.dumps(rec, indent=4))

    elif user_ch.lower() == 'status':
        stat_in = input("Enter the catefory in Status(Open/Close): ")
        for i in data:
            if stat_in in i.values():
                print(json.dumps(i, indent=4))

def deleteIncident():
    with open("incidents.json", "r") as file:
        data = json.load(file)

    new_data = [i for i in data if i["status"]!='Close']
    backup_data = [j for j in data if j["status"]=='Close']

    with open("incidents.json", "w") as file:
        json.dump(new_data, file, indent=4)

    with open("backup.json", "w") as file:
        json.dump(backup_data, file, indent=4)

    if len(backup_data) == 0:
        print("No value to be deleted")
    else:
        print("Incident deleted successfully.")


import time
import json

def updateIncident():
    with open("incidents.json", "r") as file:
        data = json.load(file)

    incident_id = int(input("Enter Incident ID to update: "))

    for inc in data:
        if inc["incident_id"] == incident_id:

            print("1. Change Status")
            print("2. Modify Description")
            print("3. Modify Severity")
            ch = input("Select option: ")

            if "updates" not in inc:
                inc["updates"] = []

            current_time = time.ctime()   

            if ch == "1":
                new_status = input("Enter New Status (Open/Investigating/Mitigated/Resolved/Close): ")
                inc["status"] = new_status
                inc["updated_at"] = current_time  

                inc["updates"].append(
                    f"Status changed to {new_status}, timestamp is {current_time}"
                )

            elif ch == "2":
                new_desc = input("Enter New Description: ")
                inc["description"] = new_desc
                inc["updated_at"] = current_time  

                inc["updates"].append(
                    f"Description changed, timestamp is {current_time}"
                )

            elif ch == "3":
                new_sev = input("Enter New Severity: ").upper()
                if new_sev in ["SEV 1", "SEV 2", "SEV 3"]:
                    inc["severity"] = new_sev
                    inc["updated_at"] = current_time  

                    inc["updates"].append(
                        f"Severity changed to {new_sev}, timestamp is {current_time}"
                    )
                else:
                    print("Invalid Severity")
                    return

            print("Incident updated!")

            with open("incidents.json", "w") as file:
                json.dump(data, file, indent=4)

            return

    print("Incident not found")


def search_service():
    ch = input("Enter the service name to be searched: ")
    with open("incidents.json", "r") as file:
        data = json.load(file)

    for i in data:
        if ch in i.values():
            print(i)

def count_incidents():
    severity_count = 0
    with open("incidents.json", "r") as file:
        data = json.load(file)

    for i in data:
        if "SEV 1" in i.values():
            severity_count += 1

    print("Severity count of SEV 1 is ", severity_count)

while(True):
    print("MENU\n 1. Create Incident\n 2. Read Incident\n 3. Delete Incident\n 4. Update Incident\n 5. Search Incident\n 6. Count of active severity (SEV 1)\n 7. Exit")
    ch = int(input("Enter your choice\n"))
    if ch==1:
        createIncident()
    elif ch==2:
        readIncident()
    elif ch==3:
        deleteIncident()
    elif ch==4:
        updateIncident()
    elif ch == 5:
        search_service()
    elif ch == 6:
        count_incidents()
    elif ch==7:
        print("Exited Successfully")
        break
    else:
        print("Enter a valid Input")
        break
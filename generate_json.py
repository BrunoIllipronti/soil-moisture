import os
import json
from datetime import datetime
from pathlib import Path

def write_json(data, filepath):
    """ This function writes json content into a json file """
    with open(filepath, "w") as f:
        content = json.dumps(data, indent=3)
        f.write(content + '\n')

def create_file(output_json):
    """ This function creates a local folder and creates a JSON file.
        Also, it validates if both exist """
    folder = "data/"
    filename = datetime.now().strftime("%d-%m-%Y") + "-moisture-read.json"
    filepath = folder+filename

    # Create Local folder
    try:
        os.mkdir(folder)
    except OSError:
        pass
        #print("Directory already created or a failure occured on directory (%s)" % folder)

    # Create Empty Json file if it doesnt exists
    if(Path(filepath)).exists():
        pass
    else:
        try:
            f = open(filepath, "a")
            f.write('{\n"moisture_iot_project":[]\n}')
            f.close()
        except Exception as e:
            print("Failure occured creating the JSON file (%s)" % e)

    # Open Json file to append current structure
    with open(filepath) as outfile:
        data = json.load(outfile)

        # Get list with all dictionaries
        temp = data['moisture_iot_project']

        # Append current structure
        temp.append(output_json)

        # Reorganize List values and re-write to JSON file
        data['moisture_iot_project'] = temp
        write_json(data, filepath)

def define_structure(sensor_name, sensor_read):
    """ This function defines a structure to write content in a JSON file """
    output_json = {
        "sensor" : sensor_name,
        "read" : sensor_read,
        "readdate" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    create_file(output_json)

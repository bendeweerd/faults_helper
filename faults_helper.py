# create fault messages & template descriptions for given triggers

import argparse
from datetime import datetime
import xlsxwriter
import csv

# construct argument parser, parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--shortcut", required=True, help="shortcut to PLC as defined in FTView Studio")
ap.add_argument("-t", "--triggers", required=True, help="path to text file containing list of triggers")
ap.add_argument("-od", "--output_directory", required=True, help="path to output directory")
ap.add_argument("-v", "--version", required=True, help="logix import/export version (0.3 for logix v33)")

args = vars(ap.parse_args())

c_shortcut = args["shortcut"]
c_triggers = args["triggers"]
c_output_dir = args["output_directory"]
c_version = args["version"]

# utility function - generate trigger string from trigger
def generate_trigger_str(trigger: str):
    return "{::[" + c_shortcut + "]" + trigger + "}"

# utility function - generate fault message from trigger & index
def generate_fault_msg(trigger: str, index: int):
    return "/*S:0 {::[" + c_shortcut + "]" + trigger + "." + str(index) + ".@Description*/"

# utility function - parse scope & description stub from trigger
def separate_scope(trigger: str):
    scope = ''
    description_stub = ''

    # check if trigger is program-scope, if so extract that scope
    if ":" in trigger:
        start_index = trigger.find(':')
        end_index = trigger.find('.')

        if start_index != -1 and end_index != -1:
            scope = trigger[start_index + 1:end_index]

    # get description stub - everything after 'faults' in trigger
    if "Faults" in trigger:
        start_index = trigger.find('Faults')
        if start_index != -1:
            description_stub = trigger[start_index + 7:]

    return [scope, description_stub]


# parse triggers from input text file
try:
    triggers = []
    with open(c_triggers, "r") as file:
        for line in file:
            trigger = line.strip()
            if trigger != '':
                triggers.append(trigger)
except:
    print("failed to parse triggers - exiting...")
    exit()

# generate timestamp for use in both filenames
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# create & populate excel file for FTView Studio import
try:
    output_filename = f"{c_output_dir}/{c_shortcut}_{timestamp}.xlsx"
    print(f"excel output: {output_filename}")
    wb = xlsxwriter.Workbook(output_filename)

    bold = wb.add_format({'bold': True})

    ws = wb.add_worksheet()
    ws.write(0, 0, "TRIGGERS", bold)

    # add trigger strings
    row = 1
    for trigger in triggers:
        trigger_str = generate_trigger_str(trigger)
        ws.write(row, 0, trigger_str)
        row = row + 1

    # add row headers
    row = row + 2
    ws.write(row, 0, "TRIGGER", bold)
    ws.write(row, 1, "TRIGGER VALUE", bold)
    ws.write(row, 2, "MESSAGE", bold)
    ws.write(row, 3, "-", bold)
    ws.write(row, 4, "DISPLAY", bold)
    ws.write(row, 5, "AUDIO", bold)
    ws.write(row, 6, "PRINT", bold)
    ws.write(row, 7, "MESSAGE TO TAG", bold)
    ws.write(row, 8, "BACKGROUND", bold)
    ws.write(row, 9, "FORGROUND", bold)

    row = row + 1

    # generate 32 fault messages per trigger, one for each bit
    for trigger in triggers:
        for i in range(32):
            message = generate_fault_msg(trigger, i)
            ws.write(row, 0, generate_trigger_str(trigger))
            ws.write(row, 1, i + 1)
            ws.write(row, 2, message)
            ws.write(row, 3, 1)
            ws.write(row, 4, 0)
            ws.write(row, 5, 0)
            ws.write(row, 6, 0)
            ws.write(row, 7, 0)
            ws.write(row, 8, 128)
            ws.write(row, 9, 16777215)
            row = row + 1

    wb.close()

except:
    print("failed to create excel file")

# create & populate csv file for Logix import
try:
    output_filename = f"{c_output_dir}/{c_shortcut}_{timestamp}.csv"
    print(f"csv output: {output_filename}")

    csv_file = open(output_filename, 'w', newline='')
    writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # add some metadata to top of file
    writer.writerow(['remark', 'CSV-Import-Export'])
    writer.writerow(['remark', f'Timestamp = {timestamp}'])
    writer.writerow(['remark', 'Automatically generated by Python script written by Ben DeWeerd - https://github.com/bendeweerd'])

    # add version to top of file - Logix needs this for the import utility to work
    writer.writerow([c_version])

    # add headers to csv
    headers = ['TYPE', 'SCOPE', 'NAME', 'DESCRIPTION', 'DATATYPE', 'SPECIFIER', 'ATTRIBUTES']
    writer.writerow(headers)

    # generate 32 descriptions per trigger, one for each bit
    for trigger in triggers:
        for i in range(32):            
            scope, stub = separate_scope(trigger)

            if scope != '':
                description = ("- SPARE - " + scope + " " + stub + '.' + str(i))
            else:
                description = ("- SPARE - " + stub + '.' + str(i))

            specifier = ("Faults." + stub + '.' + str(i))
            writer.writerow(['COMMENT', scope, 'Faults', description, '', specifier])

except:
    print("failed to create csv file")

# cleanup
csv_file.close()
print("completed. exiting...")
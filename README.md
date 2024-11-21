# Logix/Panelview Fault Template Generator

This program creates spreadsheets to simplify the process of setting up alarms on a system with an Allen-Bradley Logix PLC and a Panelview HMI project created in FactoryTalk View Studio.

The output is in a format that allows the Panelview HMI to pull fault messages directly from tag descriptions of their respective fault bits. This allows you to update the fault description in the PLC and automatically update the corresponding fault message in the HMI. In order for this to work, every fault bit referenced by the HMI **must** have a non-empty string as its description in the PLC.

The program takes a list of fault triggers (assumed to be DINTs) in .txt format as input and creates:
1. An Excel (.xlsx) file to paste into the FactoryTalk View Studio alarm setup tool. It contains references to the descripton of each fault bit.
2. A CSV (.csv) file to use with the Logix Tag Import utility. It contains a template/spare fault description for each fault bit. **Importing this into your Logix project will overwrite any previous descriptions of the specified tags**.

## Setup
1. Download & install [Python](https://www.python.org/downloads/) if you haven't already. Make sure to add Python to path/environment variables during install.
2. Run 'setup.bat' (Windows) or 'setup.sh' (Unix) to install dependencies.

## Usage
1. Create the directory you'd like to store output files in.
2. Create a .txt file listing the triggers you want to use.
3. Open a terminal in the same directory as `faults_helper.py`
4. Run `python faults_helper.py -s {plc shortcut} -t {path to trigger file} -od {path to output directory} -v {logix import/export version}`

### Example:
`python faults_helper.py -s PLC -t triggers/test_triggers.txt -od output -v 0.3`

### Command line arguments:
| Short | Long | Details | 
| --- | --- | --- |
| -s | --shortcut | shortcut to PLC as defined in FTView Studio (e.g. 'PLC') |
| -t | --triggers | path to .txt file containing list of triggers |
| -od | --output_directory | path to output directory |
| -v | --version | logix import/export version (0.3 for logix v33) |

## Example trigger file:
'test_triggers.txt'
```
Program:Global.Faults.Sensor_Fault[0]
Program:Global.Faults.Sensor_Fault[1]
Program:Global.Faults.Machine_Fault[0]
Program:Global.Faults.Machine_Fault[1]
Program:Global.Faults.Machine_Fault[2]
Program:Global.Faults.Status_Fault[0]
Program:Global.Faults.Status_Fault[1]
Program:Global.Faults.Status_Fault[2]
Program:Global.Faults.Warning

Program:TrimStation.Faults.Sensor_Fault[0]
Program:TrimStation.Faults.Sensor_Fault[1]
Program:TrimStation.Faults.Machine_Fault[0]
Program:TrimStation.Faults.Machine_Fault[1]
Program:TrimStation.Faults.Machine_Fault[2]
Program:TrimStation.Faults.Status_Fault[0]
Program:TrimStation.Faults.Status_Fault[1]
Program:TrimStation.Faults.Status_Fault[2]
Program:TrimStation.Faults.Warning

Program:Outfeed.Faults.Sensor_Fault[0]
Program:Outfeed.Faults.Sensor_Fault[1]
Program:Outfeed.Faults.Machine_Fault[0]
Program:Outfeed.Faults.Machine_Fault[1]
Program:Outfeed.Faults.Machine_Fault[2]
Program:Outfeed.Faults.Status_Fault[0]
Program:Outfeed.Faults.Status_Fault[1]
Program:Outfeed.Faults.Status_Fault[2]
Program:Outfeed.Faults.Warning

Program:Infeed.Faults.Sensor_Fault[0]
Program:Infeed.Faults.Sensor_Fault[1]
Program:Infeed.Faults.Machine_Fault[0]
Program:Infeed.Faults.Machine_Fault[1]
Program:Infeed.Faults.Machine_Fault[2]
Program:Infeed.Faults.Status_Fault[0]
Program:Infeed.Faults.Status_Fault[1]
Program:Infeed.Faults.Status_Fault[2]
Program:Infeed.Faults.Warning
```

***

Written by Ben DeWeerd.
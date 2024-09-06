# midi_tap_pro_util
MIDI Tap Pro Utility - This utility is was written to demonstrate a means of pushing and pulling raw MIDI data from a MIDI Tap Pro. It should only be used for reference.<br>
Refer to the MIDI Tap Pro user manual for detailed information regarding usage.
## Dependencies
* [Python](https://www.python.org/)
* [pyserial](https://pypi.org/project/pyserial/)
* [matplotlib](https://pypi.org/project/matplotlib/)
## Setup
There are many ways to run a python program, this is just another...
1. Clone this project
2. Open terminal and navigate to this project
3. Create virtual environment (Windows example below)
```console
py -m venv .venv
.venv\Scripts\activate
pip install pyserial
pip install matplotlib
```
4. Run the program
```console
py main.py
```
## Usage
![app](https://github.com/cssdesignllc/midi_tap_pro_util/blob/main/image/mtp_util_main.jpg)
1. Find the MTP UART using the drop down box. Note: the UART represents the assigned MIDI port.
2. Press the 'Open UART' button to open the port.
3. Activity Tab - shows graphical and tabular data received on the MIDI port.
4. MIDI Message Tab - allows building of MIDI messages and sending to the MIDI port.

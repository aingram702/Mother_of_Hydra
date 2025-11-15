# Mother_of_Hydra
An amazing GUI wrapper for the Hydra password cracker

## Usage Instructions

### Install Requirements:
Install Hydra
sudo apt-get install hydra  # Debian/Ubuntu
or
brew install hydra  # macOS

Python tkinter (usually pre-installed)
sudo apt-get install python3-tk  # if needed

### Run the GUI:
python3 hydra_gui.py

### For HTTP/HTTPS Form Attacks:
Select the appropriate attack type (HTTP/HTTPS POST/GET)
Enter target (e.g., example.com)
Set port if non-standard (80 for HTTP, 443 for HTTPS)
Configure form path (e.g., /login.php)
Set form parameters using ^USER^ and ^PASS^ placeholders
Specify failure or success string
Choose username/password (single or list)
Click "Start Attack"



Example HTTP POST Form Setup:

Target: testphp.vulnweb.com
Form Path: /login.php
Form Parameters: uname=^USER^&pass=^PASS^&submit=Login
Failure String: Wrong username or password

### Features:
✅ Multiple protocol support (HTTP, HTTPS, SSH, FTP, etc.)

✅ HTTP/HTTPS form authentication (POST/GET) 

✅ Username/password lists or single credentials 

✅ Custom headers support 

✅ Real-time output display 

✅ Thread configuration 

✅ Timeout settings 

✅ Start/Stop controls 

✅ Output saving 

Note: Use this tool only for legal penetration testing with proper authorization. Unauthorized access to systems is illegal.

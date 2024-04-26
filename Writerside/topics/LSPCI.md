# LSPCI

Start typing here...

```Python
import subprocess
import re

class VendorInfo:
    def __init__(self):
        self.command_base = ['lspci', '-v', '-s', '00:02.0', '-xxxvvv']

    def get_vendor_name(self):
        command = self.command_base.copy()

        try:
            output = subprocess.check_output(command, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{' '.join(command)}' failed with return code {e.returncode}")
            output = e.output
            return None

        hex_pattern = r'Subsystem:\s([^,]+)'
        match = re.search(hex_pattern, output, re.DOTALL)

        if match:
            vendor_id = match.group(1).strip()
            print(f"Subsystem vendor name: {vendor_id}")
            return vendor_id
        else:
            print("Subsystem vendor name not found in output.")
            return None

    def get_vendor_id(self):
        command = self.command_base

        try:
            output = subprocess.check_output(command, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{' '.join(command)}' failed with return code {e.returncode}")
            output = e.output
            return None

        hex_pattern = r'20:\s(([0-9a-f]{2}\s){15})'
        match = re.search(hex_pattern, output, re.DOTALL)

        if match:
            hex_values = match.group(1).split()
            vendor_id = hex_values[12] + " " + hex_values[13]
            print(f"Vendor ID: {vendor_id}")
            return vendor_id
        else:
            print("Vendor ID not found in output")
            return None


if __name__ == '__main__':
    vendor_info = VendorInfo()

    vendor_name = vendor_info.get_vendor_name()
    if(vendor_name is not None):
        print(f"Subsystem vendor name: {vendor_name}")

    vendor_id = vendor_info.get_vendor_id()
    if(vendor_id is not None):
        print(f"Vendor ID: {vendor_id}")
```
# LSPCI

從lspci指令的輸出中抓取指定VGA控制器的製造商信息

```Python
import subprocess
import re

class VendorInfo:
    VGA_PATTERN = r"^(\S+) VGA compatible controller: (?!Intel Corporation)"
    SUBSYSTEM_PATTERN = r'Subsystem:\s([^,]+)'
    VENDOR_ID_PATTERN = r'20:\s(([0-9a-f]{2}\s){15})'

    def get_vga_controllers(self):
        """
        從lspci指令的輸出中抓取含有"VGA compatible controller"前面的值,
        但排除 Intel Corporation 製造商

        Returns:
            list: 包含非 Intel Corporation VGA 控制器前面值的字串生成器
        """
        lspci_output = self._run_lspci()
        if lspci_output is None:
            return []

        return (match.group(1) for line in lspci_output.splitlines()
                if (match := re.match(self.VGA_PATTERN, line)))

    def get_vendor_info(self, vga_id, vendor_info_type):
        """
        從lspci指令的輸出中抓取指定VGA控制器的製造商信息

        Args:
            vga_id (str): VGA控制器的前綴值
            vendor_info_type (str): 'name' 或 'id'

        Returns:
            str: 製造商名稱或製造商ID
        """
        vendor_info_pattern = self.SUBSYSTEM_PATTERN if vendor_info_type == 'name' else self.VENDOR_ID_PATTERN
        output = self._run_lspci(extra_args=['-v', '-s', vga_id, '-xxxvvv'])
        if output is None:
            return None

        match = re.search(vendor_info_pattern, output, re.DOTALL)
        if match:
            vendor_info = match.group(1).strip()
            if vendor_info_type == 'id':
                vendor_info = ' '.join(vendor_info.split()[12:14])
            return vendor_info
        else:
            print(f"Vendor {vendor_info_type} not found in output.")
            return None

    def _run_lspci(self, extra_args=None):
        """
        執行lspci指令並返回輸出

        Args:
            extra_args (list): 額外的參數列表

        Returns:
            str: lspci指令的輸出
        """
        command = ['lspci'] + (extra_args or [])
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command '{' '.join(command)}' failed with return code {e.returncode}")
            print(e.stderr)
            return None


if __name__ == '__main__':
    vendor_info = VendorInfo()

    vga_controllers = vendor_info.get_vga_controllers()

    for vga_id in vga_controllers:
        vendor_name = vendor_info.get_vendor_info(vga_id, 'name')
        vendor_id = vendor_info.get_vendor_info(vga_id, 'id')
        print(f"ID: {vga_id}, Vendor Name: {vendor_name}, Vendor ID: {vendor_id}")
```

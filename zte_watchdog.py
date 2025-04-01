import os
import time
from zteReboot import zteRouter
import argparse

first_start = True

def is_internet_reachable():
    """Performs a ping to Google to check connectivity."""
    response = os.system("ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1")
    return response == 0

def reboot_zte(zte_ip, zte_password):
    """Reboots the ZTE router."""
    print("Connectivity lost. Rebooting ZTE router...")
    zte = zteRouter(zte_ip, zte_password)
    zte.reboot()

def reboot_router(openwrt_ip, openwrt_user, openwrt_password):
    """Reboots the OpenWrt router."""
    print("Connectivity lost. Rebooting OpenWrt router...")
    os.system(f"sshpass -p '{openwrt_password}' ssh -o StrictHostKeyChecking=no {openwrt_user}@{openwrt_ip} 'reboot'")

def monitor_internet(zte_ip, zte_password, openwrt_ip, openwrt_user, openwrt_password, first_start_timeout, ping_interval):
    """Monitors internet connectivity and handles reboot if necessary."""
    global first_start

    while True:        

        first_start_timer = 0
        while first_start:
            if is_internet_reachable():
                print("Internet is reachable, first_start = False")    
                first_start = False        
            else:
                print("First start ping failed.")

            time.sleep(10)
            first_start_timer = first_start_timer + 10
            print(f"first_start_timer:{first_start_timer}, first_start_timeout:{first_start_timeout}")
            if first_start_timer > first_start_timeout:
                print(f"first_start_timeout elapsed, internet not available. Continue execution.")
                first_start = False


            
        if is_internet_reachable():
            print("Internet is reachable.")            
        else:
            print("Ping failed. Additional attempts...")
            for attempt in range(5):
                time.sleep(2)  # Wait 2 seconds between attempts
                if is_internet_reachable():
                    print("Connectivity restored on attempt:", attempt + 1)
                    break
                else:
                    print("Ping additional attempt failed, count:", attempt + 1)

            else:
                # After 5 failed attempts
                reboot_zte(zte_ip, zte_password)
                reboot_router(openwrt_ip, openwrt_user, openwrt_password)
                print("Reboot executed")
                first_start = True    
        time.sleep(ping_interval)  # Wait ping_interval seconds before the next ping

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor internet connectivity and reboot routers if needed.")
    parser.add_argument("--zte_ip", type=str, required=True, help="IP address of the ZTE router.")
    parser.add_argument("--zte_password", type=str, required=True, help="Password for the ZTE router.")
    parser.add_argument("--openwrt_ip", type=str, required=True, help="IP address of the OpenWrt router.")
    parser.add_argument("--openwrt_user", type=str, required=True, help="Username for the OpenWrt router.")
    parser.add_argument("--openwrt_password", type=str, required=True, help="Password for the OpenWrt router.")
    parser.add_argument("--first_start_timeout", type=int, default=120, required=False, help="Wait for internet connection before start regular check")
    parser.add_argument("--ping_interval", type=int, default=10, required=False, help="Ping interval time seconds")

    args = parser.parse_args()

    monitor_internet(args.zte_ip, args.zte_password, args.openwrt_ip, args.openwrt_user, args.openwrt_password, args.first_start_timeout, args.ping_interval)
   

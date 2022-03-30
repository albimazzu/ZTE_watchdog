# zteRouterReboot
### requirements
```
python -m pip install requests js2py
```
### description
This little application simply reboots your ZTE-Router ([see some examples](https://zteaustria.com/en/internet)), currently provided by Deutsche Telekom, since it provides no API. So I did a little reverse-engineering on the login process and the reboot command.  
Just create an instance of zteRouter with the IP and the password of your router. Then call the reboot function like this:
```
zteInstance = zteRouter("127.0.0.1", "password")
zteInstance.reboot()
```

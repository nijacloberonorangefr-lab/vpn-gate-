# gate-vpn-
This is  a vpn free for bypass censure you country . this program for Linux 

here is  instruction for use 
you need python before start you must download python 
start download requirotry with this command git clone https://github.com/nijacloberonorangefr-lab/vpn-gate-.git 
start program with this command python3 import_vpngate.py 
flowers instruction in your terminal  
in to your download folder you will to see few file 
you open you seating go to network you click more you click on add a file you add. 
if you want clear you vpn you can use this command : for uuid in $(nmcli -t -f UUID,TYPE connection show | grep ':vpn$' | cut -d: -f1); do nmcli connection delete "$uuid"; done 
if you want  disble ipv6 you can use this command : sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1 after a restart become as before  
there are few serv work bad if see you was not change it is a bad serv you can change 

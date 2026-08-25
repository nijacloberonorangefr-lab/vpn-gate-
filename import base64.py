import base64
import os
import requests

dossier_telechargements = os.path.expanduser("~/Downloads")

print("📡 Récupération de la liste des serveurs VPN Gate en temps réel...")
try:
    response = requests.get("http://www.vpngate.net/api/iphone/", timeout=10)
except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit(1)

lines = response.text.split("\n")
servers = [l.split(",") for l in lines if l.startswith("vpn") or ("," in l and not l.startswith("*"))]

# 1. Analyse et comptage des pays disponibles
dispo_pays = {}
valid_raw_servers = []

for s in servers[1:]:
    if len(s) > 14 and s[14]:
        country_name = s[5]
        country_code = s[6]
        valid_raw_servers.append(s)
        
        if country_code not in dispo_pays:
            dispo_pays[country_code] = {"name": country_name, "count": 1}
        else:
            dispo_pays[country_code]["count"] += 1

print("\n🌍 --- PAYS ACTUELLEMENT DISPONIBLES --- 🌍")
# Tri des pays par nombre de serveurs décroissant
sorted_countries = sorted(dispo_pays.items(), key=lambda item: item[1]["count"], reverse=True)
for code, info in sorted_countries:
    print(f"  • {code} : {info['name']} ({info['count']} serveurs)")
print("-----------------------------------------\n")

# 2. On demande le choix à l'utilisateur
choix_pays = input("👉 Entrez le code pays (ex: JP, US, FR) ou 'ALL' : ").strip().upper()
choix_proto = input("⚙️ Entrez le protocole (UDP, TCP) ou 'ALL' : ").strip().upper()

print(f"\n🔍 Traitement des meilleurs serveurs pour {choix_pays} en {choix_proto}...")

valid_servers = []
for s in valid_raw_servers:
    ip_address = s[1] 
    country_code = s[6]
    
    if choix_pays != 'ALL' and country_code != choix_pays:
        continue
        
    try:
        config_decoded = base64.b64decode(s[14]).decode('utf-8', errors='ignore')
        
        is_udp = 'proto udp' in config_decoded.lower()
        is_tcp = 'proto tcp' in config_decoded.lower()
        
        if choix_proto == 'UDP' and not is_udp:
            continue
        if choix_proto == 'TCP' and not is_tcp:
            continue
        
        # Remplacement du DDNS par l'Adresse IP pour plus de fiabilité
        new_config = []
        for line in config_decoded.split('\n'):
            if line.strip().startswith('remote '):
                parts = line.split()
                if len(parts) >= 3:
                    line = f"remote {ip_address} {parts[2]}"
            new_config.append(line)
        
        proto_label = "UDP" if is_udp else "TCP"
        valid_servers.append({"code": country_code, "speed": int(s[4]), "config": "\n".join(new_config), "proto": proto_label})
    except Exception:
        continue

valid_servers.sort(key=lambda x: x["speed"], reverse=True)
top_servers = valid_servers[:3]

if not top_servers:
    print("❌ Aucun serveur correspondant trouvé avec ce protocole.")
else:
    print(f"✅ {len(top_servers)} excellents serveurs trouvés ! Création des fichiers...")
    
    for i, srv in enumerate(top_servers):
        # Création du fichier directement dans le bon dossier
        filename = os.path.join(dossier_telechargements, f"VPN-Gate-{srv['code']}-{srv['proto']}-{i+1}.ovpn")
        
        with open(filename, "w") as f:
            f.write(srv["config"])

    print(f"🎉 Terminé ! Les fichiers vous attendent dans votre dossier 'Downloads'.")
import json
import ipaddress
from jinja2 import Template
from collections import defaultdict

# --- Charger la topologie ---
with open("topology.json") as f:
    topo = json.load(f)

routers = topo["routers"]
links = topo["links"]
base_net = ipaddress.ip_network(topo["ip_base"])

# --- Structures internes ---
interfaces = defaultdict(list)
rip_networks = defaultdict(set)
iface_count = defaultdict(int)

current_net = base_net

# --- Calcul IP + interfaces ---
for link in links:
    a, b = link["a"], link["b"]

    hosts = list(current_net.hosts())
    ip_a = hosts[0]
    ip_b = hosts[1]

    iface_a = f"GigabitEthernet0/{iface_count[a]}"
    iface_b = f"GigabitEthernet0/{iface_count[b]}"

    iface_count[a] += 1
    iface_count[b] += 1

    interfaces[a].append({
        "name": iface_a,
        "ip": str(ip_a),
        "mask": str(current_net.netmask)
    })

    interfaces[b].append({
        "name": iface_b,
        "ip": str(ip_b),
        "mask": str(current_net.netmask)
    })

    # RIP annonce le réseau connecté
    rip_networks[a].add(str(current_net.network_address))
    rip_networks[b].add(str(current_net.network_address))

    current_net = ipaddress.ip_network(
        int(current_net.network_address) + current_net.num_addresses
    ).supernet(new_prefix=current_net.prefixlen)

# --- Charger le template ---
template = Template(open("router_rip.j2").read())

# --- Génération des configs ---
for router in routers:
    config = template.render(
        name=router,
        interfaces=interfaces[router],
        rip_networks=sorted(rip_networks[router])
    )

    with open(f"{router}.cfg", "w") as f:
        f.write(config)

print("Configurations générées avec succès.")
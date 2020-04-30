import openstack 
from os import environ as env

#openstack.enable_logging(debug=True)

conn = openstack.connect(
    region_name=env['OS_REGION_NAME'],
    auth=dict(
        auth_url=env['OS_AUTH_URL'],
        username=env['OS_USERNAME'],
        password=env['OS_PASSWORD'],
        project_id=env['OS_PROJECT_ID'],
        user_domain_id=env['OS_PROJECT_DOMAIN_ID']))

def server_list(conn):
    for server in conn.compute.servers():
        print(server.id, server.name, server.vm_state, server.hypervisor_hostname)       
    return server.name

def get_all_hosts(conn):
    all_hosts = []
    for hyper in conn.compute.hypervisors():
        hyper = conn.compute.get_hypervisor(hyper)
        if hyper.status=="enabled" and hyper.state == "up":
            all_hosts.append(hyper)
    all_hosts.sort(key=lambda x: x.name)
    return all_hosts

def print_host_list():    
    for host in get_all_hosts(conn):
        print("host_name:", host.name)        
        print("CPU total:", str(host.vcpus))
        print("CPU used_now:", str(host.vcpus_used))
        print("Memory total:", str(host.memory_size))
        print("Memory used_now:", str(host.memory_used))  

def get_instance(conn, instance_id):
    server = conn.compute.find_server(instance_id)
    if server:
        server = conn.compute.wait_for_server(server)
    return server

def print_info_instance(conn, instance_id):
    server = get_instance(conn, instance_id)
    print(server.id, server.name, server.vm_state, server.hypervisor_hostname)

def migrate_instance(conn, instance_id, target_host):
    server = get_instance(conn, instance_id)
    #print(server.id)
    #print(target_host)
    if server:
        conn.compute.live_migrate_server(server, host=target_host)

print("Testing script........................................")
print("List of server(instance)..............................")
instance_id=server_list(conn)

print("Information about instance before migrate.............")
print_info_instance(conn, instance_id)

print("List of host..........................................")
print_host_list()

print("Input target host")
target_host = input()
print(target_host)

print("Process of live migration")
print("......................................................")
migrate_instance(conn,instance_id,target_host)

print("Information about instance after migrate..............")
print_info_instance(conn, instance_id)

from ipaddress import ip_network, IPv4Network, IPv4Address
from scapy.all import sniff
from pyptables import default_tables, restore
from pyptables.rules import Rule, Accept


def set_rules(source):

    tables = default_tables()

    # # get the forward chain of the filter tables
    forward = tables['filter']['FORWARD']
    input_table = tables['filter']['INPUT']

    # any packet matching an established connection should be allowed
    forward.append(Accept(match='conntrack', ctstate='ESTABLISHED'))

    # add rules to the forward chain for DNS, HTTP and HTTPS ports
    SSH = Rule(proto='tcp', dport='22')
    input_table.append(SSH(jump='ACCEPT', source=source, comment='Allow SSH from my workstation'))

    forward.append(Accept(proto='tcp', dport='53'))
    forward.append(Accept(proto='tcp', dport='80'))
    forward.append(Accept(proto='tcp', dport='443'))

    # any packet not matching a rules will be dropped
    forward.policy = Rule.DROP
    print(input_table)


def check_packet():
    packets = sniff(count=50, iface='Wi-Fi', prn=lambda x: x.summary())
    packet_passed = []
    packet_status = []
    print(packets)
    for pkt in packets:
        if pkt.haslayer('IP'):
            source = IPv4Address(pkt['IP'].src)
            if IPv4Address(pkt['IP'].src) in ip_network('192.168.0.0/16').hosts():
                if pkt['IP'].src not in packet_passed:
                    set_rules(pkt['IP'].src)
                packet_passed.append(pkt['IP'].src)
                packet_status.append('Passed')
            else:
                packet_passed.append(pkt['IP'].src)
                packet_status.append('Dropped')
    return zip(packet_passed, packet_status)


check_packet()
from scapy.all import sniff
from .tables import set_rules
from pyptables.rules import Reject


def filter_packets():
    set_rules()
    packets = sniff(count=50, iface='Wi-Fi', prn=lambda x: x.summary())
    packet_src = []
    packet_dst = []
    packet_len = []
    packet_reject = []
    packet_encryption = []
    for pkt in packets:
        if pkt.haslayer('IP'):
            if pkt.haslayer('TCP'):
                packet_src.append(pkt['IP'].src)
                packet_dst.append(pkt['IP'].dst)
                packet_reject.append('TCP')
                packet_len.append(len(pkt))
                if pkt['TCP'].sport == 443:  # To Check HTTPS Protocol , Packet is encrypted or not
                    packet_encryption.append(True)
                else:
                    packet_encryption.append(False)
            else:
                packet_src.append(pkt['IP'].src)
                packet_dst.append(pkt['IP'].dst)
                packet_len.append(len(pkt))
                packet_reject.append('UDP/ICMP REJECTED')
                packet_encryption.append(False)

    return zip(packet_src, packet_dst, packet_len, packet_reject, packet_encryption)

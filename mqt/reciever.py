import mqttudp.engine as me

def recv_packet(pkt):
    if pkt.ptype != me.PacketType.Publish:
        print( str(pkt.ptype) + ", " + pkt.topic + "\t\t" + str(addr) )
        return
    print( pkt.topic+"="+pkt.value+ "\t\t" + str(pkt.addr) )

if __name__ == "__main__":
    me.listen(recv_packet)
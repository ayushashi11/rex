import mqttudp.engine as me

if __name__ == "__main__":
    me.send_publish( "test_topic", b"Hello, world!" )
    me.send_ping()
    me.send_subscribe(b"message")
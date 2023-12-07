from scapy.all import *
from scapy.layers.l2 import Ether

IFACE='VMware Network Adapter VMnet8'
# Define a custom protocol with necessary fields
class CustomProtocol(Packet):
    name = "CustomProtocol"
    fields_desc = [
        StrField("text", ""),
        MACField("destination_mac", ETHER_ANY),
    ]


# Function to send a message
def send_message(destination_mac, message):
    packet = Ether(dst=destination_mac) / CustomProtocol(text=message, destination_mac=destination_mac)
    packet.show()
    sendp(packet, iface=IFACE)


# Function to receive and process messages
def receive_message(packet):
    if packet.haslayer(CustomProtocol):
        custom_packet = packet[CustomProtocol]
        source_mac = packet[Ether].src
        text = custom_packet.text
        print(f"Received message from {source_mac}: {text}")


# Sniff for incoming messages
def listen_for_messages():
    while True:
        frames =sniff(iface=IFACE, prn=receive_message, count=1)
        print(frames)



# Main program loop
def main():
    while True:
        choice = input("Choose 'S' to send a message or 'R' to receive messages: ")

        if choice.upper() == 'S':
            destination_mac = input("Enter the destination MAC address: ")
            message = input("Enter the message to send: ")
            send_message(destination_mac, message)
        elif choice.upper() == 'R':
            print("Listening for messages...")
            listen_for_messages()


if __name__ == '__main__':
    main()

# Cybersecurity-Man-in-the-Middle-Attack

# Technologies
Python
* tkinter
* threading
* socket

Virtualization
* VirtualBox
* Linux Mint Xfce Image

DNS
* bind9

# Man in the Middle Scheme
Two python GUI applications were developed, and a virtual environment was configured inside VirtualBox

## Virtual Environment
The infrastructure consists of 4 virtual machines connected through a virtual network inside VirtualBox.
* 2 VMs work as the chat clients.
* 1 VM is the Man in th Middle.
* 1 VM works as the DNS of the network.

All VMs were given static IPs and the DNS was configured using bind9 as the DNS server.

| Virtual Machine | Domain Name                | IP          |
|-----------------|----------------------------|-------------|
| DNS             | DNS.seguridad.com          | 192.178.7.1 |
| Usfq            | usfq.seguridad.com         | 192.178.7.2 |
| DiegoServer     | diegoserver.seguridad.com  | 192.178.7.3 |
| AdrianServer    | adrianserver.seguridad.com | 192.178.7.4 |

## Chat application
The chat application works as a client-server application, in which two clients can communicate between each other. The chat implements Diffie-Hellman as the key exchange mechanism, and the messages transmited are encrypted using AES (128 bits) symmetric encryption.

The chat workflow is as follows:
* The first client starts listening for connections on port 50515.
* The second client asks the DNS for the IP corresponding to the domain name of the first client.
* The second client connects to the given IP on port 50515.
* Both clients reconstruct a symmetric key using Diffie-Hellman key exchange.
* Any client can send and receive encrypted messages between each other.

## Man in the Middle Application

The workflow is as follows:
* The application waits for the connection of the second client, and then connects to the first client that was already listening. 
* Key exchange is performed with each client separately.
* Every message transmitted between clients pass through the Man in the Middle.
* The messages can be modified and retransmited.

## DNS attack
In order to make effective the Man in the Middle Application, a DNS attack was simulated by changing all IPs on the DNS to the Man in the Middle IP

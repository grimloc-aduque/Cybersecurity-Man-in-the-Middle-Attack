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
* 2 virtual machines work as chat clients.
* 1 VM is the Man in the Middle.
* 1 VM works as the DNS of the network.

All VMs were given static IP addresses and the DNS was configured using bind9 as the DNS server.

| Virtual Machine | Domain Name                | IP          |
|-----------------|----------------------------|-------------|
| DNS             | DNS.seguridad.com          | 192.178.7.1 |
| Usfq            | usfq.seguridad.com         | 192.178.7.2 |
| DiegoServer     | diegoserver.seguridad.com  | 192.178.7.3 |
| AdrianServer    | adrianserver.seguridad.com | 192.178.7.4 |

## Chat application
The chat application works like a client-server application, in which two clients can communicate with each other. The chat implements Diffie-Hellman as a key exchange mechanism, and transmitted messages are encrypted using AES (128-bit) symmetric encryption.

The chat workflow is as follows:
* The first client starts listening for connections on port 50515.
* The second client asks the DNS for the IP corresponding to the domain name of the first client.
* The second client connects to the given IP on port 50515.
* Both clients reconstruct a symmetric key using the Diffie-Hellman key exchange.
* Any client can send and receive encrypted messages to each other.

<img src="https://github.com/grimloc-aduque/Cybersecurity-Man-in-the-Middle-Attack/blob/main/images/chatGUI.png" style="width:400px;"/>


## Man in the Middle Application

The workflow is as follows:
* The application waits for the second client to connect and then connects to the first client that was already listening.
* The exchange of keys is done with each client separately.
* All messages transmitted between clients go through the Man in the Middle.
* Messages can be modified and retransmitted.

<img src="https://github.com/grimloc-aduque/Cybersecurity-Man-in-the-Middle-Attack/blob/main/images/man_in_the_middle.png" style="width:400px;"/>


## DNS attack
For the Man in the Middle application to be effective, a DNS attack was simulated by changing all IPs in the DNS to the Man in the Middle IP.

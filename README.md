# ⌨️**Real-time messaging facility over a computer network**⏳

## 💡**Main idea**💡
It is necessary to develop a program (console or graphical) for exchanging text messages that works on a local network in peer-to-peer mode.
Each messaging participant (node) is identified by an IP address and an arbitrary name that is specified by the user (via a command line parameter, a configuration file, or in any other way). Names are not required to be unique.
Each node uses UDP to form a list of active nodes (IP addresses and names):
* **once started, the node sends a broadcast packet containing its name to notify other nodes on the network of its connection to the network;**
* **other nodes that receive such a packet establish a TCP connection for messaging with the sender and send their name over it for identification in the chat.**<br>
A new client can join the chat at any time.
Messages are exchanged using TCP in a logically shared space: each node maintains one TCP connection with every other node and sends its messages to all nodes in the network. Disabling a node must be correctly handled by other nodes.

## 🔎**How to Install**🔍
* **Clone project to your folder:** `git clone https://github.com/amarjin6/chat-room.git`

## 🛠**How to Use**🛠

# Python Socket Message
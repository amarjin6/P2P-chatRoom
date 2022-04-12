![GitHub commit merge status](https://img.shields.io/github/commit-status/amarjin6/P2P-chatRoom/master/b61f31554014e906f4d82dfa5fd83c095d005c47?color=purple&logo=pypi)
![GitHub language count](https://img.shields.io/github/languages/count/amarjin6/P2P-chatRoom?logo=python&logoColor=green)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/amarjin6/P2P-chatRoom?color=gree&logo=gitbook&logoColor=yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/amarjin6/P2P-chatRoom?color=yellow&logo=Stackbit)
![GitHub watchers](https://img.shields.io/github/watchers/amarjin6/P2P-chatRoom?logo=wechat)

# ⏰**Real-time messaging facility over a computer network**⏳

## 💡**Main idea**💡
Create a software tool for exchanging text messages that works on a local network in peer-to-peer mode.
Each messaging participant (node) is identified by an IP address and an arbitrary name that is specified by the user (via a command line parameter). Names are not required to be unique.
Each node uses UDP to form a list of active nodes (IP addresses and names):
* **once started, the node sends a broadcast packet containing its name to notify other nodes on the network of its connection to the network;**
* **other nodes that receive such a packet establish a TCP connection for messaging with the sender and send their name over it for identification in the chat.**<br>

A new client can join the chat at any time.
Messages are exchanged using TCP in a logically shared space: each node maintains one TCP connection with every other node and sends its messages to all nodes in the network. Disabling a node must be correctly handled by other nodes.

## 🔎**How to Install**🔍
* **Clone project to your folder:** `git clone https://github.com/amarjin6/chat-room.git`
* **Check for updates and install all necessary [plugins](https://github.com/amarjin6/P2P-chatRoom/tree/master/requirements)**
* **Run project in terminal:** `python chat.py [host] [username]`

## 🛠**How to Use**🛠
* **Run the project in your terminal with different IP's**
* **Send message to your chat member**
* **Don't forget to read rules and active commands!**
* **Completed!**

## 🥽**Preview**🥽

# Python Socket Thread
*This project has been created as part of the 42 curriculum by shanazaw.*

# NetPractice

## Description

NetPractice is a practical introduction to computer networking. Its goal is to make small simulated networks function correctly by configuring IPv4 addresses, subnet masks, and routing information in a browser-based training interface.

The project contains 10 levels. Each level presents a network diagram and communication objectives. Completing the exercises develops reasoning about addressing, local networks, and communication through routers and gateways. The networks are simulated; their configuration is performed inside the provided interface.

## Instructions

### Installation and execution

Requirements: a web browser, a shell to run the supplied script, and Python 3 for the fallback web server. The supplied training interface does not require compiling a student program.

1. Download the official training archive from the NetPractice project page on the 42 intranet. The provided evaluation checklist identifies it as `net_practice.1.9.tgz`.
2. Extract the archive into a directory of your choice.
3. Open a terminal in the extracted directory containing `run.sh` and run:

   ```sh
   ./run.sh
   ```

   The script starts a local web server and opens the training interface in your browser.

If the script does not work, run the following command from the extracted directory containing the interface files:

```sh
python3 -m http.server 49242
```

Then open [http://localhost:49242](http://localhost:49242) in your browser. If you choose another port, use the same port in the browser URL. Keep the server running while using the interface; press `Ctrl+C` in its terminal to stop it.

### Exporting configurations and submission

1. Enter your 42 login (`shanazaw`) in the training interface to use your personal configuration.
2. Complete each level and click **Check again** to verify that all communication objectives are met.
3. Before moving to the next level, click **Get my config** to download the completed configuration. Repeat this for all 10 levels.

For submission, place the 10 exported configuration files, one per level (`level1.json` through `level10.json`), at the root of your Git repository alongside `README.md`.

## Resources

AI supported README writing and discussions to check my understanding of networking concepts. See [AI Usage](#ai-usage).

### Provided project materials

- Official NetPractice subject (version 6.3).
- Official browser-based training interface, distributed as `net_practice.1.9.tgz`, including `run.sh` and the 10 exercises.

### Books

- [ネットワークはなぜつながるのか 第2版 — 知っておきたいTCP/IP、LAN、光ファイバの基礎知識](https://bookplus.nikkei.com/atcl/catalog/07/P83110/)
- [マスタリングTCP/IP 入門編（第6版）](https://www.ohmsha.co.jp/book/9784274224478.html)

### Networking concepts covered

| Concept | Overview |
| --- | --- |
| TCP/IP addressing | NetPractice focuses on IPv4 addressing within the TCP/IP suite. An IPv4 address is 32 bits, usually written as four decimal octets, and identifies a network interface. 
| Subnet masks | A mask identifies the network portion of an IPv4 address and helps determine whether a destination belongs to a directly connected subnet. CIDR notation expresses the prefix length, such as `/24` for `255.255.255.0`. 
| Default gateways | A default gateway is the next-hop router used when no more specific route matches a destination. In these Ethernet networks, the next hop must be reachable on the outgoing interface's local subnet. The IPv4 default route is `0.0.0.0/0`.
| Routers and switches | Routers forward IP packets between networks using routing information. Layer 2 switches connect devices within a local network and forward Ethernet frames using MAC addresses. 
| OSI layers | The OSI model separates networking responsibilities into seven layers: physical, data link, network, transport, session, presentation, and application. IP routing belongs to layer 3; ordinary Ethernet switching belongs to layer 2. 

## AI Usage

AI was used to help write this README and as a discussion partner to check my understanding of networking concepts.

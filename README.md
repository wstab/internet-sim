# Internet Sim

This program simulates connections between servers and ip addresses.

## Getting Started

### Installing

* Clone the repo
```
git clone https://github.com/wstab/wstab-internet-sim.git
```

### Executing program

* Run Program
* Enter following commands (exclude brackets):
  - create server
    ```
    create-server [domain name] [ip address]
    ```
  - display servers
    ```
    display-servers
    ```
  - set current server location/position
    ```
    set-server [domain name]
    ```
  - create connection between two servers, including time it takes to ping 
    ```
    create-connection [domain name 1] [domain name 2] [ping time]
    ```
  - display time it takes to ping the given server
    ```
    ping [domain name or ip address]
    ```
  - display route to get to the given server
    ```
    tracert [domain name or ip address]
    ```

# hetznercloud-py

A Python SDK for the new (and wonderful) Hetzner cloud service.

* [State](#state)
* [Usage](#documentation)
    * [Getting started](#getting-started)
        * [A note on actions](#a-note-on-actions)
        * [Standard exceptions](#standard-exceptions)
        * [Constants](#constants)
            * [Server types](#server-types)
            * [Images](#image-types)
            * [Datacentres](#datacentre-constants)
    * [Servers](#servers)
        * [Top level actions](#server-top-level-actions)
            * [Get all servers](#get-all-servers)
            * [Get all servers by name](#get-all-servers-by-name)
            * [Get server by id](#get-server-by-id)
            * [Create server](#create-server)
        * [Modifier actions (applies to a specific server)](#server-modifier-actions)

## State

The SDK is currently under development. Please switch to the develop branch of this project if you wish to see the 
progress made on it so far.

## Documentation

This library is organised into two components: the first, a set of actions that retrieve an actionable component. 
These actionable components (for example servers) each have their own methods that modify their own (and only their own)
behaviour. 

### Getting started

In order to get started with the library, you first need an instance of it. This is very simple, and uses a number
of hand-crafted helper functions to make configuration changes.

```
from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient

configuration = HetznerCloudClientConfiguration().with_api_key("YOUR-API-KEY").with_api_version(1)
client = HetznerCloudClient(configuration)
```

The client is your entry point to the SDK.

#### A note on actions

Methods that modify server state (such as creating, imaging, snapshotting, deleting etc) generally return a tuple. The
first value of this tuple is normally the object type modified (i.e. a server), whilst the second value is the action. 

The `HetznerCloudAction` object (second value in the tuple) can be used to wait for certain states to be achieved before
continuing. For more information, see the [Actions](#actions) section.

#### Constants

The SDK contains a number of helpful constants that save you having to look up things such as image names, server types
and so on. 

*Please note:* I endeavour to keep the constants up to date, but sometimes it is just not possible. Should
this happen, feel free to use plain-ole strings (i.e. cx11 for the smallest cloud instance) in their place until I get
around to deploying the update.

##### Server types

Constants that represent the server types available to users.

* `SERVER_TYPE_1CPU_2GB` - The smallest type with 1 CPU core, 2GB of RAM and a 20GB SSD disk.
* `SERVER_TYPE_1CPU_2GB_CEPH` - The same as above but with a 20GB CEPH network-attached disk.
* `SERVER_TYPE_2CPU_4GB` - Type with 2 CPU cores, 4GB of RAM and a 40GB SSD disk.
* `SERVER_TYPE_2CPU_4GB_CEPH` - The same as above but with a 40GB CEPH network-attached disk.
* `SERVER_TYPE_2CPU_8GB` - Type with 2 CPU cores, 8GB of RAM and a 80GB SSD disk.
* `SERVER_TYPE_2CPU_8GB_CEPH` - The same as above but with a 80GB CEPH network-attached disk.
* `SERVER_TYPE_4CPU_16GB` - Type with 4 CPU cores, 16GB of RAM and a 160GB SSD disk.
* `SERVER_TYPE_4CPU_16GB_CEPH` - The same as above but with a 160GB CEPH network-attached disk.
* `SERVER_TYPE_8CPU_32GB` - The largest type with 8 CPU cores, 32GB of RAM and a 240GB SSD disk.
* `SERVER_TYPE_8CPU_32GB_CEPH` - The same as above but with a 240GB CEPH network-attached disk.

##### Image types

Constants that represent the standard images available to users.

* `IMAGE_UBUNTU_1604` - Ubuntu 16.04 LTS
* `IMAGE_DEBIAN_9` - Debian 9.3
* `IMAGE_CENTOS_7` - CentOS 7.4
* `IMAGE_FEDORA_27` - Fedora 27

##### Datacentre constants

Constants that represent the datacentres available to users.

* `DATACENTER_FALKENSTEIN_1` - Falkenstein 1 DC 8
* `DATACENTER_NUREMBERG_1` - Nuremberg 1 DC 3

#### Standard exceptions

A number of standard exceptions can be thrown from the methods that interact with the Hetzner API.

* `HetznerAuthenticationException` - raised when the API returns a 401 Not Authorized or 403 Forbidden status code.
* `HetznerInternalServerErrorException` - raised when the API returns a 500 status code.


### Servers

The servers top level action is accessible through the `client.servers()` method. You must use one of the methods in
the object returned by this top level action in order to modify the state of individual servers.

#### Server top level actions

##### Get all servers

All servers associated with the API key you provided can be retrieved by calling the `get_all()` top level action method.

```
all_servers = client.servers().get_all() # gets all the servers as a generator
all_servers_list = list(client.servers().get_all()) # gets all the servers as a list
```

#### Get all servers by name

By calling the `get_all(name="my-server-name")` method (with the optional `name` parameter entered), you can bring back
the servers that have the name entered.

```
all_servers = client.servers().get_all(name="foo") # gets all the servers as a generator
all_servers_list = list(client.servers().get_all(name="foo")) # gets all the servers as a list
```

#### Get server by id

If you know the id of the server you wish to retrieve you can use this method to retrieve that specific server.

```
try:
    server = client.servers().get(1)
catch HetznerServerNotFoundException:
    print("Woops, server not found!")
```

This method throws a `HetznerServerNotFoundException` if the following conditions are satisfied:

* The id passed into the method is not an integer or is not greater than 0.
* The API returns a 404 indicating that the server could not be found.

#### Create server

To create a server, you can call the `create` top level action method. This method accepts a number of parameters (some
are optional, some aren't).

```
my_new_server, create_action = client.servers().create(name="My required server name", # REQUIRED
    server_type=hetznercloud.SERVER_TYPE_1CPU_2GB, # REQUIRED
    image=hetznercloud.IMAGE_UBUNTU_1604, # REQUIRED
    datacenter=hetznercloud.DATACENTER_FALKENSTEIN_1,
    start_after_create=True,
    ssh_keys=["my-ssh-key-1", "my-ssh-key-2"],
    user_data="rm -rf a-file")
    
print(my_new_server.id)
```

This method throws a `HetznerInvalidArgumentException` if the required parameters detailed above are not specified with
valid values.

This method throws a `HetznerServerActionException` if an error is returned whilst creating the server.
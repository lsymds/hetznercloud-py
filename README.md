# Hetzner Cloud Python SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/elsyms/hetznercloud-py.svg?branch=develop)](https://travis-ci.org/elsyms/hetznercloud-py) 

A Python 3 SDK for the new (and wonderful) Hetzner cloud service.

* [Contributing](#contributing)
* [Changelog](#changelog)
* [Usage](#documentation)
    * [Installation](#installation)
    * [Getting started](#getting-started)
        * [A note on actions](#a-note-on-actions)
        * [Standard exceptions](#standard-exceptions)
        * [Constants](#constants)
            * [Server Statuses](#server-statuses)
            * [Action statuses](#action-statuses)
            * [Server types](#server-types)
            * [Images](#image-types)
            * [Datacenters](#datacenter-constants)
            * [Backup windows](#backup-windows)
            * [Image types](#image-types)
            * [Image sorts](#image-sorts)
    * [Datacenters](#datacenters)
        * [Top level actions](#datacenter-top-level-actions)
            * [Get all datacenters](#get-all-datacenters)
            * [Get all datacenters by name](#get-all-datacenters-by-name)
            * [Get a datacenter by id](#get-datacenter-by-id)
    * [Floating IPs](#floating-ips)
        * [Top level actions](#floating-ips-top-level-actions)
            * [Create](#create-floating-ip)
            * [Get all floating IPs](#get-all-floating-ips)
            * [Get floating IPs by id](#get-floating-ip-by-id)
        * [Modifier actions](#floating-ips-modifier-actions)
            * [Assign to server](#assign-floating-ip-to-server)
            * [Change description](#change-floating-ip-description)
            * [Change reverse DNS entry](#change-floating-ip-reverse-dns-entry)
            * [Delete floating IP](#delete-floating-ip)
            * [Unassign from server](#unassign-floating-ip-from-server)
    * [Images](#images)
        * [Top level actions](#images-top-level-actions)
            * [Get all images](#get-all-images)
            * [Get image by id](#get-image-by-id)
        * [Modifier actions (applies to a specific image)](#image-modifier-actions)
            * [Update image](#update-image)
            * [Delete image](#delete-image)
    * [Isos](#isos)
        * [Top level actions](#isos-top-level-actions)
            * [Get all isos](#get-all-isos)
            * [Get all isos by name](#get-all-isos-by-name)
            * [Get an iso by id](#get-iso-by-id)
    * [Locations](#locations)
        * [Top level actions](#locations-top-level-actions)
            * [Get all locations](#get-all-locations)
            * [Get all locations by name](#get-all-locations-by-name)
            * [Get a location by id](#get-location-by-id)
    * [Servers](#servers)
        * [Top level actions](#server-top-level-actions)
            * [Get all servers](#get-all-servers)
            * [Get all servers by name](#get-all-servers-by-name)
            * [Get server by id](#get-server-by-id)
            * [Create server](#create-server)
        * [Modifier actions (applies to a specific server)](#server-modifier-actions)
            * [Attach an ISO](#attach-iso)
            * [Change reverse DNS](#change-reverse-dns)
            * [Change name](#change-server-name)
            * [Change type](#change-server-type)
            * [Delete](#delete-server)
            * [Detach ISO](#detach-iso)
            * [Disable rescue mode](#disable-rescue-mode)
            * [Enable backups](#enable-server-backups)
            * [Enable rescue mode](#enable-rescue-mode)
            * [Image](#image-server)
            * [Power on](#power-on)
            * [Power off](#power-off)
            * [Rebuild from image](#rebuild-from-image)
            * [Reset](#reset-server)
            * [Reset root password](#reset-root-password)
            * [Shutdown](#shutdown-server)
            * [Wait for status](#wait-for-server-status)
    * [Server types](#server-size-types)
        * [Top level actions](#server-types-top-level-actions)
            * [Get all server types](#get-all-server-types)
            * [Get all server types by name](#get-all-server-types-by-name)
            * [Get a server type by id](#get-server-type-by-id)
    * [SSH Keys](#ssh-keys)
        * [Top level actions](#ssh-keys-top-level-actions)
            * [Create SSH key](#create-ssh-key)
            * [Get all SSH keys](#get-all-ssh-keys)
            * [Get all SSH keys by name](#get-all-ssh-keys-by-name)
            * [Get SSH key by id](#get-ssh-key-by-id)
        * [Modifier actions](#ssh-modifier-actions)
            * [Delete SSH key](#delete-ssh-key)
            * [Update SSH key](#update-ssh-key)

## Contributing

Open source contributions are more than welcome to be submitted to this repository and every issue and pull request will be
promptly reviewed and evaluated on its suitability to be merged into the main branches. 

## Changelog

### v1.0.3

* Fixes an issue with the 8GB server constants having the wrong type. See [issue 15](https://github.com/elsyms/hetznercloud-py/issues/15)

### v1.0.2

* Updated the README to show supported Python version and this changelog section. 
* Fixed an issue with status codes returned from server actions.
* Fixed an issue where the body is null when sending a POST request.
* Added the new Helsinki DC as a constant.
* Added a check to the shared API requestor that checks for the 429 rate limited status code and returns a suitable exception.
* Added an alias for datacenters, as my Britishness got the best of me when creating this library.

## Documentation

This library is organised into two components: the first, a set of actions that retrieve an actionable component. 
These actionable components (for example servers) each have their own methods that modify their own (and only their own)
behaviour. 

### Installation

Install the library into your environment by executing the following command in your terminal:

```bash
pip install hetznercloud
```

### Getting started

In order to get started with the library, you first need an instance of it. This is very simple, and uses a number
of hand-crafted helper functions to make configuration changes.

```python
from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient

configuration = HetznerCloudClientConfiguration().with_api_key("YOUR-API-KEY").with_api_version(1)
client = HetznerCloudClient(configuration)
```

The client is your entry point to the SDK.

#### A note on actions

Methods that modify server state (such as creating, imaging, snapshotting, deleting etc) generally return a tuple. The
first value of this tuple is normally the object type modified (i.e. a server), whilst the second value is the action. 

The `HetznerCloudAction` object (second value in the tuple) can be used to wait for certain states of that invoked task 
to be achieved before continuing. For more information, see the [Actions](#actions) section.

#### Constants

The SDK contains a number of helpful constants that save you having to look up things such as image names, server types
and so on. 

*Please note:* I endeavour to keep the constants up to date, but sometimes it is just not possible. Should
this happen, feel free to use plain-ole strings (i.e. cx11 for the smallest cloud instance) in their place until I get
around to deploying the update.

##### Server statuses

Constants that represent the different statuses a server can have.

* `SERVER_STATUS_RUNNING` - The server is running.
* `SERVER_STATUS_INITIALIZING` - The server is running its initialisation cycle.
* `SERVER_STATUS_STARTING` - The server is starting after being powered off.
* `SERVER_STATUS_STOPPING` - The server is stopping (shutting down).
* `SERVER_STATUS_OFF` - The server is turned off.
* `SERVER_STATUS_DELETING` - The server is being deleted.
* `SERVER_STATUS_MIGRATING` - The server is being migrated.
* `SERVER_STATUS_REBUILDING` - The server is being rebuilt.
* `SERVER_STATUS_UNKNOWN` - The status of the server is unknown.`

##### Action statuses

Constants that represent the different statuses an action can have.

* `ACTION_STATUS_RUNNING` - The action is currently running.
* `ACTION_STATUS_SUCCESS` - The action completed successfully.
* `ACTION_STATUS_ERROR` - The action terminated due to an error.

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
* `DATACENTER_HELSINKI_1` - Helsinki 1 DC 2

##### Backup windows

Constants that represent backup windows. 

* `BACKUP_WINDOW_10PM_2AM` - Backup window between 10PM and 2AM
* `BACKUP_WINDOW_2AM_6AM` - Backup window between 2AM and 6AM
* `BACKUP_WINDOW_6AM_10AM` - Backup window between 6AM and 10AM
* `BACKUP_WINDOW_10AM_2PM` - Backup window between 10AM and 2PM
* `BACKUP_WINDOW_2PM_6PM` - Backup window between 2PM and 6PM
* `BACKUP_WINDOW_6PM_10PM` - Backup window between 6PM and 10PM

##### Floating IP types

Constants that represent floating IP types

* `FLOATING_IP_TYPE_IPv4` - IPv4 floating IP
* `FLOATING_IP_TYPE_IPv6` - IPv6 floating IP

##### Image types

Constants that represent image types.

* `IMAGE_TYPE_BACKUP` - A manual backup of a server, which is then bound to the server it was created from.
* `IMAGE_TYPE_SNAPSHOT` - A snapshot of a server that can be used to create other servers. 

##### Image sorts

Constants that define the different ways that images can be sorted.

* `SORT_BY_ID_ASC` - Sorts the images by their numerical id in ascending order.
* `SORT_BY_ID_DESC` - Sorts the images by their numerical id in descending order.
* `SORT_BY_NAME_ASC` - Sorts the images by their name in ascending character order.
* `SORT_BY_NAME_DESC` - Sorts the images by their name in descending character order.
* `SORT_BY_CREATED_ASC` - Sorts the images by their created date in ascending order.
* `SORT_BY_CREATED_DESC` - Sorts the images by their created date in descending order.

#### Standard exceptions

A number of standard exceptions can be thrown from the methods that interact with the Hetzner API.

* `HetznerAuthenticationException` - raised when the API returns a 401 Not Authorized or 403 Forbidden status code.
* `HetznerInternalServerErrorException` - raised when the API returns a 500 status code.
* `HetznerActionException` - raised when an action on something yields an error in the JSON response or the status code
is not what was expected.
* `HetznerInvalidArgumentException` - raised when a required argument of the method is not specified correctly. The
exception will detail the failing parameter.

### Datacenters

#### Top level actions

The datacenter top level action can be retrieved by calling the `datacenters()` method on the `HetznerCloudClient`
instance.

##### Get all datacenters

To retrieve all of the datacenters available on the Hetzner Cloud service, simply call the `get_all()` method, passing
in no parameters.

*NOTE: This method returns a generator, so if you wish to get all of the results instantly, you should encapsulate the
call within the `list()` function*

```python
all_dcs_generator = client.datacenters().get_all()
for dc in all_dcs_generator:
    print(dc.id)
    
all_dcs_list = list(client.datacenters().get_all())
print(all_dcs_list)
```

##### Get all datacenters by name

To get all datacenters filtered by a name, call the `get_all()` method with the name parameter populated.

```python
all_dcs = list(client.datacenters().get_all(name="fsn1-dc8"))
print(all_dcs)
```

##### Get datacenter by id

To get a datacenter by id, simply call the `get()` method on the datacenter action, passing in the id of the datacenter
you wish to get information for.

```python
datacenter = client.datacenters().get(1)
print(datacenter.name)
```

### Floating IPs

#### Floating IPs top level actions

##### Create floating IP

To create a floating IP, simply call the `create()` method with the parameters detailed below. 

*NOTE: If you do not specify `server`, then you must specify `home_location`, or vice versa.*

```python
new_floating_ip = client.floating_ips().create(type=FLOATING_IP_TYPE_IPv4,
    server=42,
    description="My new floating IP")
    
" or...
 
new_floating_ip = client.floating_ips().create(type=FLOATING_IP_TYPE_IPv4,
    home_location="fep1",
    description="My new floating IP")
```

##### Get all floating IPs

```python
floating_ips = client.floating_ips().get_all()
for ip in floating_ips:
    print(ip.id)
```

##### Get floating IP by id

```python
floating_ip = client.floating_ips().get(1)
print(floating_ip.id)
```

#### Floating IPs modifier actions

##### Assign floating IP to server

```python
floating_ip = client.floating_ips().get(1)
action = floating_ip.assign_to_server(2)
action.wait_until_status_is(ACTION_STATUS_RUNNING)
```

##### Change floating IP description

```python
floating_ip = client.floating_ips().get(1)
action = floating_ip.change_description("My new floating IP v2")
```

##### Change floating IP reverse DNS entry

```python
floating_ip = client.floating_ips().get(1)
action = floating_ip.change_reverse_dns_entry("192.168.1.1", "www.google.com")
action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Delete floating IP

```python
floating_ip = client.floating_ips().get(1)
action = floating_ip.delete()
```

##### Unassign floating IP from server

```python
floating_ip = client.floating_ips().get(1)
action = floating_ip.unassign_from_server()
```

### Images

#### Images top level actions

##### Get all images

To retrieve all of the images available on the Hetzner Cloud service, simply call the `get_all()` method, passing
in no parameters.

There are also a number of parameters on this method that allow you to filter and sort images.

```python
images = client.images().get_all(sort=SORT_BY_ID_ASC)
for image in images:
    print(image.id)
```

##### Get image by id

To get an image by its id, simply call the `get()` method, passing in the id of the image you wish to retrieve.

```python
image = client.images().get(1)
print(image.id)
```

#### Images modifier actions

##### Update image

To update an image's description or type, call the `update()` method with the description of the image and/or the type
of the image, should you wish to update them. Both parameters are optional.

```python
image = client.images().get(1)
image.update(description="my description", type=IMAGE_TYPE_SNAPSHOT)
```

##### Delete image

To delete an image, call the `delete()` method. NOTE: Only images of type 'snapshot' or 'backup' can be deleted (so,
you cannot delete the images provided by Hetzner!).

```python
image = list(client.images().get_all(name="my-first-image"))[0]
image.delete()
```

### ISOs

#### Top level actions

The iso top level action can be retrieved by calling the `isos()` method on the `HetznerCloudClient`
instance.

##### Get all ISOs

To retrieve all of the isos available on the Hetzner Cloud service, simply call the `get_all()` method, passing
in no parameters.

*NOTE: This method returns a generator, so if you wish to get all of the results instantly, you should encapsulate the
call within the `list()` function*

```python
isos = client.isos().get_all()
for l in isos:
    print(l.id)
    
isos = list(client.isos().get_all())
print(isos)
```

##### Get all ISOs by name

To get all isos filtered by a name, call the `get_all()` method with the name parameter populated.

```python
isos = list(client.isos().get_all(name="virtio-win-0.1.141.iso"))
print(isos)
```

##### Get ISO by id

To get an iso by id, simply call the `get()` method on the datacenter action, passing in the id of the iso
you wish to get information for.

```python
iso = client.isos().get(1)
print(iso.name)
```

### Locations

#### Top level actions

The location top level action can be retrieved by calling the `locations()` method on the `HetznerCloudClient`
instance.

##### Get all locations

To retrieve all of the locations available on the Hetzner Cloud service, simply call the `get_all()` method, passing
in no parameters.

*NOTE: This method returns a generator, so if you wish to get all of the results instantly, you should encapsulate the
call within the `list()` function*

```python
all_locs_generator = client.locations().get_all()
for l in all_locs_generator:
    print(l.id)
    
all_locs_list = list(client.locations().get_all())
print(all_locs_list)
```

##### Get all locations by name

To get all locations filtered by a name, call the `get_all()` method with the name parameter populated.

```python
all_locs = list(client.locations().get_all(name="fsn1"))
print(all_locs)
```

##### Get location by id

To get a location by id, simply call the `get()` method on the datacenter action, passing in the id of the location
you wish to get information for.

```python
location = client.locations().get(1)
print(location.name)
```


### Servers

The servers top level action is accessible through the `client.servers()` method. You must use one of the methods in
the object returned by this top level action in order to modify the state of individual servers.

#### Server top level actions

##### Get all servers

All servers associated with the API key you provided can be retrieved by calling the `get_all()` top level action method.

```python
all_servers = client.servers().get_all() # gets all the servers as a generator
all_servers_list = list(client.servers().get_all()) # gets all the servers as a list
```

##### Get all servers by name

By calling the `get_all(name="my-server-name")` method (with the optional `name` parameter entered), you can bring back
the servers that have the name entered.

```python
all_servers = client.servers().get_all(name="foo") # gets all the servers as a generator
all_servers_list = list(client.servers().get_all(name="foo")) # gets all the servers as a list
```

##### Get server by id

If you know the id of the server you wish to retrieve you can use this method to retrieve that specific server.

```python
try:
    server = client.servers().get(1)
except HetznerServerNotFoundException:
    print("Woops, server not found!")
```

This method throws a `HetznerServerNotFoundException` if the following conditions are satisfied:

* The id passed into the method is not an integer or is not greater than 0.
* The API returns a 404 indicating that the server could not be found.

##### Create server

To create a server, you can call the `create` top level action method. This method accepts a number of parameters (some
are optional, some aren't).

```python
server_a, create_action = client.servers().create(name="My required server name", # REQUIRED
    server_type=SERVER_TYPE_1CPU_2GB, # REQUIRED
    image=IMAGE_UBUNTU_1604, # REQUIRED
    datacenter=DATACENTER_FALKENSTEIN_1,
    start_after_create=True,
    ssh_keys=["my-ssh-key-1", "my-ssh-key-2"],
    user_data="rm -rf a-file")
server_a.wait_until_status_is(SERVER_STATUS_RUNNING) 
```

#### Server modifier actions

Once you have an instance of the server (retrieved by using one of the "Top level actions" above), you are able to
perform different modifier actions on them.

##### Attach ISO

To attach an ISO to the server, call the `attach_iso()` method on the `HetznerCloudServer` object, specifying either the
name or the ID of the ISO you wish to attach to the server (these can be retrieved by using the `isos().get_all()`
method on the client).

*NOTE: Constants will **not** be provided for the ISOs, as they are too dynamic and likely to change.*

```python
server = client.servers().get(1)
iso_action = server.attach_iso("virtio-win-0.1.141.iso")
iso_action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Change reverse DNS

To change the reverse DNS record associated with the server, call the `change_reverse_dns_entry()` method on the
`HetznerCloudServer` object, specifying the IP address you wish to add a record for and the reverse DNS record.

*NOTE: If you leave the `dns_pointer` parameter as `None`, the reverse DNS record will be reverted back to what Hetzner
set it as when they created your server.*

```python
server = client.servers().get(1)
action = server.change_reverse_dns_entry("192.168.1.1", "www.google.com")
```

##### Change server name

To change the server name, call the `change_name()` method on the `HetznerCloudServer` object, specifying a valid name
as the first and only parameter.

*NOTE: This method does not return an action, so it is assumed that the update is processed immediately. You can verify
this assumption by renaming the server, immediately retrieving it by its id and checking the name of the retrieved
server is what you renamed it to.*

```python
server = client.servers().get(1)
server.change_name("my-new-server-name")
```

##### Change server type

To change the server type (i.e. from a small, to a large instance), call the `change_type()` method on the
`HetznerCloudServer` object, specifying the new server type as the first parameter and whether to resize the
disk as the second parameter.

*NOTE: Your server needs to be powered off in order for this to work.*

*NOTE: If you wish to downgrade the server type in the future, make sure you set the `upgrade_disk` parameter to False.
Not doing this will result in an error being thrown should you try to downgrade in the future.*

```python
server = client.servers().get(1)
action = server.change_type(SERVER_TYPE_2CPU_4GB, False)

action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Delete server

To delete the server, call the `delete()` method on the `HetznerCloudServer` object.

```python
server = client.servers().get(1)
action = server.delete()

# Wait until the delete action has completed.
action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Detach ISO

To detach the ISO from the server (if there is one present), call the `detach_iso()` method on the `HetznerCloudServer`
object. 

*NOTE: Calling this method when no ISO is attached to the server will succeed and not throw an error.*

```python
server = client.servers.get(1)
action = server.detach_iso()

action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Disable rescue mode

To disable rescue mode on the server, simply call the `disable_rescue_mode()` on the server object.

*NOTE*: Although the API documentation says an error will be returned if rescue mode is already disabled, we have found
this is not the case.

```python
server = client.servers().get(1)
disable_action = server.disable_rescue_mode()

disable_action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Enable server backups

To enable server backups, simply call the `enable_backups()` method on the server object with your chosen backup window.

```python
server = client.servers().get(1)
action = server.enable_backups(BACKUP_WINDOW_2AM_6AM)
```

This method throws a `HetznerActionException` if the backup window is not one of the valid choices (see:
https://docs.hetzner.cloud/#resources-server-actions-post-11).

##### Enable rescue mode

To enable rescue mode, simply call the `enable_rescue_mode()` method on the server object. You can specify a rescue
image and an array of SSH keys to load into it.

*NOTE*: If you use the FreeBSD rescue image, you will not be able to load in any SSH keys.

*NOTE:* If you want to use the rescue mode, you will need to reboot your server. This method will not automatically
do that for you.

```python
server = client.servers().get(1)
root_password, enable_action = server.enable_rescue_mode(rescue_type=RESCUE_TYPE_LINUX32, ssh_keys=["my-ssh-key"])

enable_action.wait_until_status_is(ACTION_STATUS_SUCCESS)

print("Your root password for the rescue mode is %s" % root_password)
```

##### Image server

To image a server (i.e. create a backup or a snapshot), call the `image()` method on the server object. You can specify
the description of the server and the type of image you are creating. Possible image types are as follows:

* `backup` - An image that is bound to the server and deleted when the server is. **Only available when server backups
are enabled**.
* `snapshot` - An image created independent of the server and billed seperately.

```python
server = client.servers().get(1)
image_id, image_action = server.image("My backup image", type=IMAGE_TYPE_BACKUP)

image_action.wait_until_status_is(ACTION_STATUS_SUCCESS)

print("The new backup image identifier is %s" % image_id)
``` 

##### Power on

To power a server on, simply call the `power_on()` method on the server object.

##### Power off

To power a server off, simply call the `power_off()` method on the server object.

##### Rebuild from image

To rebuild a server from an image, simply call the `rebuild_from_image()` method on the server object, passing in the
image id or name you wish to overwrite the server with.

*NOTE: This method will destroy **all** data on the server*

```python
server = client.servers().get(1)
action = server.rebuild_from_image(IMAGE_UBUNTU_1604)

action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Reset server

To reset a server (equivelent to pulling the power cord and plugging it back in), simply call the `reset()` method on
the server object.

```python
server = client.servers().get(1)
action = server.reset()
action.wait_until_status_is(ACTION_STATUS_SUCCESS)
```

##### Reset root password

To reset the password of the Root account on a server, simply call the `reset_root_password()` method on the server
object. 

```python
server = client.servers().get(1)
root_password, reset_action = server.reset_root_password()

print("The new root password is %s" % root_password)
```

##### Shutdown server

To shutdown a server gracefully, simply call the `shutdown()` method on the server object.

*NOTE: The OS on the server you are trying to shut down must support ACPI.*

```python
server = client.servers().get(1)
server.shutdown()
```

##### Wait for server status

You can wait for a server to have a particular status by calling the `wait_until_status_is(desired_status)` method on
the server object.

This method will loop a set number of times (defined by the `attempts` parameter) and pause each time for one second
(or a timespan defined by modifying the wait_seconds parameter) until the number of attempts is exceeded
or the condition matches.

This is useful when you want to ensure your server is of a particular state before performing any actions on it.

```python
server = client.servers().get(1)

try:
    server.wait_until_status_is(SERVER_STATUS_OFF, attempts=50, wait_seconds=10)
except HetznerWaitAttemptsExceededException:
    print("Server status was not updated in 50 attempts") 
```

This method throws a `HetznerWaitAttemptsExceededException` should the amount of attempts be exceeded with the condition
still being unmet.

### Server size types

#### Top level actions

The server types top level action can be retrieved by calling the `server_types()` method on the `HetznerCloudClient`
instance.

##### Get all server types

To retrieve all of the server types available on the Hetzner Cloud service, simply call the `get_all()` method, passing
in no parameters.

*NOTE: This method returns a generator, so if you wish to get all of the results instantly, you should encapsulate the
call within the `list()` function*

```python
types = client.server_types().get_all()
for l in types:
    print(l.id)
    
types = list(client.server_types().get_all())
print(types)
```

##### Get all server types by name

To get all server types filtered by a name, call the `get_all()` method with the name parameter populated.

```python
server_types = list(client.server_types().get_all(name="cx11"))
print(server_types)
```

##### Get server type by id

To get a server type by id, simply call the `get()` method on the datacenter action, passing in the id of the server type
you wish to get information for.

```python
stype = client.server_types().get(1)
print(stype.name)
```

### SSH keys

#### SSH keys top level actions

##### Create SSH key

To create an SSH key, call the `create()` method on the `HetznerCloudSSHKeysAction` with the name and the public key of
the SSH key you wish to add.

```python
new_ssh_key = client.ssh_keys().create(name="My new SSH key", public_key="abcdef")
print(new_ssh_key.fingerprint)
```

##### Get all SSH keys

To get all SSH keys, call the `get_all()` method. NOTE: This object returned from this method is a generator.

```python
ssh_keys = client.ssh_keys().get_all()
for ssh_key in ssh_keys:
    print(ssh_key.id)
```

##### Get all SSH keys by name

To get all SSH keys by their name, call the `get_all()` method, but pass in the name of the SSH key you wish to search
for. 

```python
ssh_keys = list(client.ssh_keys().get_all(name="My SSH key"))
for ssh_key in ssh_keys:
    print(ssh_key.id)
```

##### Get SSH key by id

```python
ssh_key = client.ssh_keys().get(1)
print(ssh_key.id)
```

#### SSH keys modifier actions

##### Delete SSH key

To delete an SSH key, call the `delete()` method on the SSH key object.

```python
ssh_key = client.ssh_keys().get(1)
ssh_key.delete()
```

##### Update SSH key

To update an SSH key's name, call the `update()` method on the SSH key object.

```python
ssh_key = client.ssh_keys().get(1)
ssh_key.update(name="Foo")
```
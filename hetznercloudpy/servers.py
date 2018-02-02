class HetznerCloudServersAction(object):
    """
    This action contains all top-level calls related to servers. Specific server-related calls (such as deleting or
    imaging a server) are done by first retrieving the server (by using the get_all or get methods in this class) and
    then calling the required method on the object returned.

    Example:
        # To delete the server, you first have to retrieve it.
        my_server = client.servers().get(32)

        # And then you can delete it.
        my_server.delete()
    """

    def get_all(self, name=None):
        """
        Retrieves all of the servers associated with the API key's project, but also allows you to filter by name.

        :param name: The name to filter the servers by.
        :return: An array of server objects.
        """
        pass

    def get(self, server_id):
        """
        Gets a server by its defined id.

        :param server_id: The server's id.
        :return: A server object if the server exists, or a HetznerServerNotFoundException.
        """
        pass


class HetznerCloudServer(object):
    def power_on(self):
        pass

    def power_off(self):
        pass

    def soft_reboot(self):
        pass

    def reset(self):
        pass

    def shutdown(self):
        pass

    def change_name(self, new_name):
        pass

    def delete(self):
        pass

    def reset_root_password(self):
        pass

    def enable_rescue_mode(self):
        pass

    def disable_rescue_mode(self):
        pass

    def image(self, description=None, image_type="snapshot"):
        pass


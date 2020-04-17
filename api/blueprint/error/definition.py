"""Class-based error definitions.
"""


class NotFound(Exception):
    """Error raised when resources are not found.
    """

    def __init__(self, resource_name, id_, parameter=None):
        """Constructor.

        :param resource_name: the name of the resource requested (e.g. block).
        :type resource_name: string.
        :param id_: the id of the missing resource.
        :type id_: integer.
        :param parameter: the parameter that caused the error if any.
        :type parameter: string.
        """
        self.status = 404
        self.code = "resource_not_found"
        self.type = "invalid_request"
        self.message = f"No such {resource_name}: {id_}."
        self.parameter = parameter
        self.url = None
        super(NotFound, self).__init__()

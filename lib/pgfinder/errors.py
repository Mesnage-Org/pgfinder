class UserError(ValueError):
    """A ValueError raised by invalid user input.

    UserError messages are intended for direct consumption by the end-user, so
    the message text should make it clear what's gone wrong and which steps the
    user can take to resolve the problem.
    """

Welcome to dotmailer's documentation!
=====================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    account
    address_books
    campaigns
    connection
    constants
    contact_data_fields
    contact_score
    contacts
    exceptions
    program_enrolments
    programs
    survey_fields
    surveys
    templates
    transactional_emails


Getting started
===============

Just to show you how easy it is to get up and running, simply import the Account object and tell it to setup a connection
using your username and password.

.. code-block:: python

    from dotmailer.account import Account
    Account.setup_connection("API USERNAME", "API PASSWORD")

By calling the static function :func:`setup_connection`, you associate your API username and password with the connection
object.  This connection object is called automatically by the rest of the library when making calls to DotMailer's API.

From then on, you won't need to interact with the connection object, just use the higher level objects like
:class:`Contact` e.g.

.. code-block:: python

    from dotmailer.contact import Contact

    # Create a new contact
    my_contact = Content(email='test@test.com')
    my_contact.create()


Each of these high level objects have a different **required** attributes which need to be set before you can perform
certain tasks.  In the previous example, email is the only required attribute to be able to create a new contact.  However,
if you want to work with a campagin object then you need to specify name, from name, html content and plain text content
when creating the instance.  For further information about which attributes are required please look at the
documentation for each class as well as `DotMailer's API <https://developer.dotmailer.com/docs/>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

********
pyiCloud
********

.. image:: https://travis-ci.org/picklepete/pyicloud.svg?branch=master
    :alt: Check out our test status at https://travis-ci.org/picklepete/pyicloud
    :target: https://travis-ci.org/picklepete/pyicloud

.. image:: https://img.shields.io/pypi/v/pyicloud.svg
    :alt: Library version
    :target: https://pypi.org/project/pyicloud

.. image:: https://img.shields.io/pypi/pyversions/pyicloud.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pyicloud

.. image:: https://pepy.tech/badge/pyicloud
    :alt: Downloads
    :target: https://pypi.org/project/pyicloud

.. image:: https://requires.io/github/Quentame/pyicloud/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Quentame/pyicloud/requirements/?branch=master

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Formated with Black
    :target: https://github.com/psf/black

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :alt: Join the chat at https://gitter.im/picklepete/pyicloud
    :target: https://gitter.im/picklepete/pyicloud?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

PyiCloud is a module which allows pythonistas to interact with iCloud webservices. It's powered by the fantastic `requests <https://github.com/kennethreitz/requests>`_ HTTP library.

At its core, PyiCloud connects to iCloud using your username and password, then performs calendar and iPhone queries against their API.


Authentication
==============

Authentication without using a saved password is as simple as passing your username and password to the ``PyiCloudService`` class:

>>> from pyicloud import PyiCloudService
>>> api = PyiCloudService('jappleseed@apple.com', 'password')

In the event that the username/password combination is invalid, a ``PyiCloudFailedLoginException`` exception is thrown.

You can also store your password in the system keyring using the command-line tool:

>>> icloud --username=jappleseed@apple.com
ICloud Password for jappleseed@apple.com:
Save password in keyring? (y/N)

If you have stored a password in the keyring, you will not be required to provide a password when interacting with the command-line tool or instantiating the ``PyiCloudService`` class for the username you stored the password for.

>>> api = PyiCloudService('jappleseed@apple.com')

If you would like to delete a password stored in your system keyring, you can clear a stored password using the ``--delete-from-keyring`` command-line option:

>>> icloud --username=jappleseed@apple.com --delete-from-keyring

**Note**: Authentication will expire after an interval set by Apple, at which point you will have to re-authenticate. This interval is currently two months.

Two-step and two-factor authentication (2SA/2FA)
************************************************

If you have enabled two-factor authentications (2FA) or `two-step authentication (2SA) <https://support.apple.com/en-us/HT204152>`_ for the account you will have to do some extra work:

.. code-block:: python

    if api.requires_2fa:
        print "Two-factor authentication required."
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            sys.exit(1)

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
    elif api.requires_2sa:
        import click
        print "Two-step authentication required. Your trusted devices are:"

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print "  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber')))

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print "Failed to send verification code"
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print "Failed to verify verification code"
            sys.exit(1)


Contacts
========

You can access your iCloud contacts/address book through the ``contacts`` property:

>>> for c in api.contacts.all():
>>> print c.get('firstName'), c.get('phones')
John [{u'field': u'+1 555-55-5555-5', u'label': u'MOBILE'}]

Note: These contacts do not include contacts federated from e.g. Facebook, only the ones stored in iCloud.

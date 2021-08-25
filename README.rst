***************
icloud-contacts
***************

This project started as a fork of `pyicloud <https://github.com/picklepete/pyicloud>`_.

It allows you to run jobs to update their contacts programmatically.

Extension to pyicloud
=====================

You can get all of your contacts using pyicloud, but the module has no way of updating them.

This project allows you to:

- update contacts

If the future, I would like te support:

- creating and deleting contacts
- creating and deleting groups
- adding and removing users from groups

Motivation
==========

I've always wanted an easier way to manage my contacts, and have sought a way to do so programmatically.
Since the majority of my contacts are on my phone, I wanted to target iCloud.
Unfortunately, Apple does not provide a public api to allow for this functionality, so my best bet was to work off of pyicloud.

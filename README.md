# laptop

When using an old Intel MacBook Pro as a Debian server a few years back (~2019), I found there were some changes needed to keep it from going to sleep and to control the backlight depending upon the state of the lid.

This repo configures lid handlers in systemd `logind.conf`, and adds a `backlightd` service to handle the lid/backlight triggers.

`backlightd` is a Python script that monitors the lid, controls the backlight, and tries to be fancy by fading changes.

I suppose I could make this into a deb package, but this seemed small enough to just keep simple.

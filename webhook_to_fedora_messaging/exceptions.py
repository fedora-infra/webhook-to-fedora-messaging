# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


class ConfigError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
    
class SignatureMatchError(Exception):
    pass


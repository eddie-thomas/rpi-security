# -*- coding: UTF-8 -*-

#
# @copyright Copyright © 2018 - 2023 by Edward K Thomas Jr
# @license GNU GENERAL PUBLIC LICENSE https://www.gnu.org/licenses/gpl-3.0.en.html
#

import CameraSecurity

if __name__ == "__main__":
    """Main file"""
    try:
        CameraSecurity.CameraSecurity(23)
    except BaseException:
        print("process killed")

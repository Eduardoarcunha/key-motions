"""
Overview: This is a demo code for using the key-motions library.
"""

import sys
import keymotions as km

json_file = sys.argv[1]

k = km.KeyMotions()
k.set_motions_from_json(json_file)
k.run()

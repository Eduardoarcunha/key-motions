import key_motions as km
import sys

json_file = sys.argv[1]

k = km.KeyMotions()
k.set_motions_from_json(json_file)
k.run()

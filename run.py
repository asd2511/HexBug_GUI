from GUI import GUI
from glob import glob
import json


n_video = 1

if __name__ == "__main__":
    for jsonPath in glob("SR_Anno//*.sr"):
    # jsonPath = "SR_Anno//training0{}.sr".format(str(n_video))
        with open(jsonPath, 'r') as f:
            selfLabel = json.load(f)
        gui = GUI(selfLabel)
        gui.root.mainloop()
        with open(jsonPath, 'w') as outfile:
            json.dump(selfLabel,  outfile, sort_keys=True, indent=4,)
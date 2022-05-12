import numpy as np
import cv2
import json
from glob import glob
import matplotlib.pyplot as plt

if __name__ == "__main__":


    for maskFolder in glob("mask-OF//*"):
        videoIdx = int(maskFolder.split("training")[1])
        with open("Annotation//training0{}.traco".format(str(videoIdx)), 'r') as f:
            label = json.load(f)

        baseInfo = {"name": videoIdx,
                    "videoPath": "Training videos//training0{}.mp4".format(str(videoIdx)),
                    "videoLen": label["rois"][-1]["z"] }

        selfLabel = {"info": baseInfo}
        for info in label["rois"]:
            if not str(info["z"]) in selfLabel.keys():
                selfLabel[str(info["z"])] = {"hexBug": []}
            selfLabel[str(info["z"])]["hexBug"].append({
                                        "id": info["id"],
                                        "pos": info["pos"]
                                        })


        for maskImgPath in glob(maskFolder+"//*.jpg"):
            idx = int(maskImgPath.split("mask_")[1].split(".")[0])-1
            print(maskImgPath)
            if str(idx) not in selfLabel.keys(): continue
            selfLabel[str(idx)]["mask"] ={
                                            "picked": False,
                                            "path": maskImgPath,
                                        }

        with open('SR_Anno//training0{}.sr'.format(str(videoIdx)), 'w') as outfile:
            json.dump(selfLabel,  outfile, sort_keys=True, indent=4,)

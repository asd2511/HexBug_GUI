import tkinter as tk
import numpy as np
import PIL.Image
import PIL.ImageTk
import cv2

class GUI():

    def __init__(self,dicts):
        self.root = tk.Tk()
        self.root.title("main window")
        self.idx = tk.IntVar()
        # video relevents
        self.dicts = dicts
        videoPath = dicts["info"]["videoPath"]

        self.sz = None

        cap = cv2.VideoCapture(videoPath)
        self.video = []
        while 1:
            ret, frame = cap.read()
            if ret:
                if self.sz is None:
                    print(frame.shape)
                    if frame.shape[0]>1000:
                        self.sz = [int(frame.shape[1]/2),int(frame.shape[0]/2)]
                    else:
                        self.sz = [int(frame.shape[1]),int(frame.shape[0])]
                self.video.append(cv2.resize(frame,self.sz))
            else:
                break
        print(videoPath, dicts["0"]["mask"]["path"])


        initFrame = self.video[0]
        self.Img = self.cv2PIL(initFrame)
        # 4 image + 2
        self.Label = tk.Label(self.root, image=self.Img)
        self.Label.grid(row=1, column=1, padx=0, pady=0, columnspan=1, rowspan=2)

        # class button
        # # !place
        # yes = tk.Button(self.root, text='\n    yes     \n', command=self.button_yes
        #     )
        # yes.grid(row=1, column=2, padx=2, pady=2, columnspan=1, rowspan=1)
        # no = tk.Button(self.root, text='\n     no     \n', command=self.button_no
        #     )
        # no.grid(row=2, column=2, padx=2, pady=2, columnspan=1, rowspan=1)
        self.scale = tk.Scale(self.root,#label='sss',
            from_=0,to=dicts["info"]["videoLen"]-1,
            resolution=1,
            orient=tk.HORIZONTAL,
            length = initFrame.shape[1],
            variable=self.idx,
            bg="red",
            command = self.scaleFunc,
            )
        self.scale.grid(row=3, column=1, padx=0, pady=0, columnspan=1, rowspan=1)

        self.root.bind_all("<a>",self.button_yes)
        self.root.bind("<z>",self.button_no)
        self.root.bind("<Left>",self.prev)
        self.root.bind("<Right>",self.next)

    def next(self,x):
        idx = int(self.idx.get())
        if idx < self.dicts["info"]["videoLen"]-1:
            self.scale.set(idx+1)

    def prev(self,x):
        idx = int(self.idx.get())
        if idx > 0:
            self.scale.set(idx-1)

    def updateImg(self):
        self.Label.configure(image=self.Img )
        self.Label.image = self.Img

    def cv2PIL(self, img):
        return PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(np.uint8(img)).convert('RGB'))


        # show()
    def button_yes(self,x):
        idx = int(self.idx.get())
        self.dicts[str(idx)]["mask"]["picked"] = True

    def button_no(self,x):
        idx = int(self.idx.get())
        self.dicts[str(idx)]["mask"]["picked"] = False

    def scaleFunc(self,idx):
        idx = int(idx)
        mask = cv2.imread(self.dicts[str(idx)]["mask"]["path"])
        if (mask.shape[0]>mask.shape[1]) != (self.video[idx].shape[0]>self.video[idx].shape[1]):
            mask = np.rot90(mask,-1)

        mask = cv2.resize(mask,self.sz)
        frame = self.video[idx] * mask

        self.Img = self.cv2PIL(frame)

        if self.dicts[str(idx)]["mask"]["picked"]:
            self.scale.configure(bg="green" )
        else:
            self.scale.configure(bg="red" )

        self.updateImg()


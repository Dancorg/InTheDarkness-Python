
class obs:
    def __init__(self,x,y,w,h,color,material = 0):
        self.data = {'x':x,'y':y,'w':w,'h':h,'color':color,'borders':[0,0,0,0],'material':material}
        self.data['borders'][0] = x - w/2 #left
        self.data['borders'][1] = x + w/2 #right
        self.data['borders'][2] = y - h/2 #top
        self.data['borders'][3] = y + h/2 #bottom

    def get_pos(self):
        return (self.data['x'],self.data['y'])

    def get_pos_size(self):
        return (self.data['x']-self.data['w']/2,self.data['y']-self.data['h']/2,self.data['w'],self.data['h'])

    def set_pos(self,x,y):
        self.data['x'] = x
        self.data['y'] = y

    def get_color(self):
        return self.data['color']

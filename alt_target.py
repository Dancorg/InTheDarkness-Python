class alt_target:
    def __init__(self, owner, x, y, w, h):
        self.data = {'x': x,'y': y,'w': w,'h':h,'owner': owner}
        self.illum = True

    def update(self,t):
        #pygame.draw.circle(screen,(100,255,100,255),(int(self.data['x']),int(self.data['y'])),10,0)
        if self.data['owner'].seg:
            self.data['x'] = t.data['x']
            self.data['y'] = t.data['y']

    def return_to_owner(self):
        self.data['x'] = self.data['owner'].data['x']
        self.data['y'] = self.data['owner'].data['y']


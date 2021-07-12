class Dino:
    def __init__(self,brain):
        self.score=0
        self.alive=True
        self.y=0
        self.inertia=0
        self.brain=brain
    def move(self,distance_nearest,speed):
        self.score+=1
        self.y+=self.inertia
        self.inertia-=0.5
        if self.y<0:
            self.y=0
            self.inertia=0
        jump_scale=self.y/130
        speed_scale=speed/30000
        #inertia_scale=self.inertia/10

        brain=self.brain.feedAll([jump_scale,speed_scale,distance_nearest])
        decision=self.getMaxResult(brain)
        if decision==0:
            self.jump()
        elif decision==1:
            self.down()

    def jump(self):
        if self.y==0:
            self.inertia=11
    def down(self):
        if self.y>0:
            self.inertia-=3
    def dead(self):
        self.alive=False
        #scores.append()
    def getMaxResult(self,results):
        return results.index(max(results))

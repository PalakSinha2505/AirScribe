class Smoother:
    def __init__(self, alpha=0.15):  
        self.alpha = alpha
        self.prev_x = None
        self.prev_y = None

    def smooth(self, x, y):
        if self.prev_x is None:
            self.prev_x, self.prev_y = x, y
            return x, y

        smooth_x = self.prev_x + self.alpha * (x - self.prev_x)
        smooth_y = self.prev_y + self.alpha * (y - self.prev_y)

        self.prev_x, self.prev_y = smooth_x, smooth_y

        return int(smooth_x), int(smooth_y)
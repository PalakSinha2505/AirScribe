class Smoother:
    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.prev_x = None
        self.prev_y = None

    def smooth(self, x, y):
        # Initialize
        if self.prev_x is None:
            self.prev_x, self.prev_y = x, y
            return x, y

        # Adaptive smoothing (slightly better stability)
        dx = abs(x - self.prev_x)
        dy = abs(y - self.prev_y)

        dynamic_alpha = self.alpha

        # If movement is large → less smoothing (more responsive)
        if dx > 20 or dy > 20:
            dynamic_alpha = 0.4
        else:
            dynamic_alpha = self.alpha

        smooth_x = self.prev_x + dynamic_alpha * (x - self.prev_x)
        smooth_y = self.prev_y + dynamic_alpha * (y - self.prev_y)

        self.prev_x, self.prev_y = smooth_x, smooth_y

        return int(smooth_x), int(smooth_y)
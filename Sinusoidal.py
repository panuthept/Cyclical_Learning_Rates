import math


class Sinusoidal:
    def __init__(self, max_lr, base_lr, stepsize, decline_mode="none", gamma=0.9):
        assert decline_mode.lower() == "none" or \
               decline_mode.lower() == "half" or \
               decline_mode.lower() == "exp", \
            "decline_mode must be either 'none', 'half' or 'exp'"
        super().__init__()

        self.max_lr = max_lr
        self.base_lr = base_lr
        self.stepsize = stepsize
        self.decline_mode = decline_mode.lower()
        self.gamma = gamma
        self.step = 0

    def __call__(self, step):
        # Caluclate current cycle
        cycle = math.floor(1 + step / (2 * self.stepsize))
        # Calculate current max_lr
        if self.decline_mode == "half":
            max_lr = self.max_lr - (self.max_lr - self.base_lr) * (1 - 1 / (2 ** (cycle - 1)))
        elif self.decline_mode == "exp":
            max_lr = self.base_lr + (self.max_lr - self.base_lr) * (self.gamma ** (cycle - 1))
        else:
            max_lr = self.max_lr
        # Calculate learning rate
        x = step / (2 * self.stepsize) - cycle + 1
        deg = 360 * x - 90
        lr = self.base_lr + (max_lr - self.base_lr) * (math.sin(math.radians(deg)) + 1) / 2

        return lr


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    clr = Sinusoidal(0.01, 0.001, 20)
    lrs = []
    for step in range(201):
        lrs.append(clr(step))
    plt.plot(lrs)
    plt.show()

    clr = Sinusoidal(0.01, 0.001, 20, decline_mode="half")
    lrs = []
    for step in range(201):
        lrs.append(clr(step))
    plt.plot(lrs)
    plt.show()

    clr = Sinusoidal(0.01, 0.001, 20, decline_mode="exp")
    lrs = []
    for step in range(201):
        lrs.append(clr(step))
    plt.plot(lrs)
    plt.show()

    clr = Sinusoidal(0.01, 0.001, 20, decline_mode="exp", gamma=0.7)
    lrs = []
    for step in range(201):
        lrs.append(clr(step))
    plt.plot(lrs)
    plt.show()
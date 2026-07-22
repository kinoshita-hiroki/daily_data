import random

from game.domain.skills.attack import Attack


class Rampage(Attack):
    def use(self, actor, targets, battle):
        if not self.check_cost(actor, battle):
            return

        self.pay_cost(actor)

        for i in range(3):
            target = random.choice(targets)
            self.apply(actor, target, battle)

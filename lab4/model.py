import numpy.random as nr


class UniformGenerator:
    def __init__(self, a, b):
        if not 0 <= a <= b:
            raise ValueError('The parameters should be in range [a, b]')
        self._a = a
        self._b = b

    def generate(self):
        return nr.uniform(self._a, self._b)


class NormalGenerator:
    def __init__(self, m, sigma):
        self._m = m
        self._sigma = sigma

    def generate(self):
        return nr.normal(self._m, self._sigma)


class Model:
    def __init__(self, dt, req_count, reenter_prob, queue_count):
        self.dt = dt
        self.req_count = req_count
        self.reenter_prob = reenter_prob

        self.queue = 0
        self.queue_len_max = queue_count
        self.reenter = 0
        self.missed = 0

    def check_len_max(self):
        if self.queue > self.queue_len_max:
            self.queue -= 1
            self.missed += 1
            # self.queue_len_max = self.queue

    def add_to_queue(self):
        self.queue += 1
        self.check_len_max()

    def rem_from_queue(self, is_reenter=True):
        if self.queue == 0:
            return 0

        self.queue -= 1

        if is_reenter and nr.sample() < self.reenter_prob:
            self.reenter += 1
            self.add_to_queue()

        return 1

    def event_based_modelling(self, a, b, m, d):
        req_generator = UniformGenerator(a, b)
        req_processor = NormalGenerator(m, d)

        req_done_count = 0
        t_generation = req_generator.generate()
        t_processor = t_generation + req_processor.generate()

        while req_done_count < self.req_count:
            if t_generation <= t_processor:
                self.add_to_queue()
                t_generation += req_generator.generate()
            elif t_generation >= t_processor:
                req_done_count += self.rem_from_queue(True)
                t_processor += req_processor.generate()

        return self.req_count, self.reenter, self.missed

    def time_based_modelling(self, a, b, m, d):
        req_generator = UniformGenerator(a, b)
        req_processor = NormalGenerator(m, d)

        req_done_count = 0
        t_generation = req_generator.generate()
        t_processor = t_generation + req_processor.generate()

        t_curr = 0
        while req_done_count < self.req_count:
            if t_generation <= t_curr:
                self.add_to_queue()
                t_generation += req_generator.generate()
            if t_curr >= t_processor:
                if self.queue > 0:
                    req_done_count += self.rem_from_queue(True)
                    t_processor += req_processor.generate()
                else:
                    t_processor = t_generation + req_processor.generate()

            t_curr += self.dt

        return self.req_count, self.reenter, self.missed

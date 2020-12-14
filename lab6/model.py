import numpy.random as nr
from enum import Enum


class ProcessorType(Enum):
    PROFESSOR = 1
    MASTER = 2


class UniformGenerator:
    def __init__(self, m, d):
        self._a = m - d
        self._b = m + d
        if not 0 <= self._a <= self._b:
            raise ValueError('Параметры должны удовлетворять условию 0 <= a <= b')

    def generate(self):
        return nr.uniform(self._a, self._b)


class ConstGenerator:
    def __init__(self, m):
        if m <= 0:
            raise ValueError('Параметр должен быть больше 0')
        self._m = m

    def generate(self):
        return self._m


class Processor:
    def __init__(self, generator, processor_type):
        self._generator = generator
        self._time = 0
        self._type = processor_type

    def generate(self):
        return self._generator.generate()

    def set_time(self, time):
        self._time = time

    def get_time(self):
        return self._time

    def get_type(self):
        return self._type


class Model:
    def __init__(self, dt, req_count, reenter_prob=0.3):
        self.dt = dt
        self.req_count = req_count
        self.reenter_prob = reenter_prob

        self.queue = 0
        self.queue_len_max = 0
        self.reenter = 0
        self.missed = 0

    def check_len_max(self):
        if self.queue > self.queue_len_max:
            self.queue_len_max = self.queue

    def add_to_queue(self):
        self.queue += 1
        self.check_len_max()

    def rem_from_queue(self, is_reenter):
        result = 1
        if self.queue == 0:
            return 0

        self.queue -= 1

        if is_reenter == ProcessorType.MASTER and nr.sample() < self.reenter_prob:
            self.reenter += 1
            self.add_to_queue()
            result = 0

        return result

    def time_based_modelling(self, client_m, client_d,
                             op1_m, op1_d, op2_m, op2_d,
                             count1, count2, time_limit):
        req_generator = UniformGenerator(client_m, client_d)
        processors = []
        for i in range(count1):
            processors.append(Processor(UniformGenerator(op1_m, op1_d), ProcessorType.PROFESSOR))

        for i in range(count2):
            processors.append(Processor(UniformGenerator(op2_m, op2_d), ProcessorType.MASTER))

        req_done_count = 0
        t_generation = req_generator.generate()

        for processor in processors:
            tmp = processor.generate()
            processor.set_time(t_generation + tmp)

        generated_req = 0
        t_curr = 0
        while t_curr <= time_limit:
            if t_generation <= t_curr:
                if generated_req < self.req_count:
                    self.add_to_queue()
                    t_generation += req_generator.generate()
                    generated_req += 1
            for processor in processors:
                if t_curr >= processor.get_time():
                    if self.queue > 0:
                        req_done_count += self.rem_from_queue(processor.get_type())
                        processor.set_time(processor.get_time() + processor.generate())
                    else:
                        processor.set_time(t_generation + processor.generate())
            t_curr += self.dt

        return round(self.queue / generated_req, 4), self.queue, self.reenter, req_done_count, generated_req

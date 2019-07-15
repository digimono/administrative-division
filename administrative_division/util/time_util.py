# -*- coding: utf-8 -*-

import random
import time


class Wait:

    @staticmethod
    def wait_seconds(min_seconds, max_seconds):
        rnd_seconds = random.uniform(min_seconds, max_seconds)
        time.sleep(rnd_seconds)

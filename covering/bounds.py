"""Counting and iterated Schönheim bounds, exact integer arithmetic only."""
from math import comb
from .verify import parameters


def lower_bounds(v, k, t):
    parameters(v, k, t)
    b, steps = 1, []
    for i in range(t - 1, -1, -1):
        b = ((v - i) * b + k - i - 1) // (k - i)
        steps.append({'v': v-i, 'k': k-i, 't': t-i, 'bound': b})
    return {'counting': (comb(v,t) + comb(k,t) - 1)//comb(k,t),
            'schonheim': b, 'steps': steps}

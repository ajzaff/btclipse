import randomselection.utils


def g(i, f, f_prime, tau_a, tau_l):
    """Probability of ``i^{th}'' rejected address given it was also rejected on the ``i-1^{th}'' try.

    :param i: (int) try number
    :param f: (float) fraction of adversarial addresses in tried
    :param f_prime: ||connected addresses|| / ||tried table|| (at best, 8/64^2)
    :param tau_a: (duration) round length
    :param tau_l: (duration) time invested in attack
    :return: (float)
    """
    p_0 = randomselection.utils.acceptprob(i, 0)
    p_a = randomselection.utils.acceptprob(i, tau_a)
    p_l = randomselection.utils.acceptprob(i, tau_l)
    return (1 - p_a) * f + (1 - p_0) * f_prime + (1 - p_l) * (1 - f - f_prime)


def q(f, f_prime, tau_a, tau_l, n=100):
    """Adverserial address accepted with probability ``q''

    :param f: (float) fraction of adversarial addresses in tried
    :param f_prime: ||connected addresses|| / ||tried table|| (at best, 8/64^2)
    :param tau_a: (duration) round length
    :param tau_l: (duration) time invested in attack
    :param n: (int) iterations to perform
    :return: (float)
    """
    s = 0
    for r in range(1, n + 1):
        m = randomselection.utils.acceptprob(r, tau_a)
        prod = 1
        for i in range(1, r):
            prod *= g(i, f, f_prime, tau_a, tau_l)
        s += f * m * prod
    return s


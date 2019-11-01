from .ValidationIndices import *
import math

class RandIndex(PairCountingScore):
    def paircounting_score(N00, N11, N, **kwargs):
        return (N00 + N11) / N

class AdjustedRandIndex(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, N, **kwargs):
        term = (N11 + N10)*(N11 + N01)/(N)
        return Fraction(N11 - term,
                        N11 + (N10 + N01)/2-term)

class MirkinMetric(PairCountingScore):
    isdistance = True
    def paircounting_score(N01, N10, **kwargs):
        return N10 + N01

class JaccardIndex(PairCountingScore):
    def paircounting_score(N00, N11, N, **kwargs):
        return Fraction(N11, N - N00)

class JaccardDistance(PairCountingScore):
    isdistance = True
    def paircounting_score(N00, N11, N, **kwargs):
        return 1-Fraction(N11, N - N00)

class HubertIndex(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, N, **kwargs):
        return (N11 + N00 - N10 - N01) / N

class WallaceIndex(PairCountingScore):
    def paircounting_score(N10, N11, **kwargs):
        return Fraction(N11, N11 + N10)

class FowlkesAndMallowIndex(PairCountingScore):
    def paircounting_score(N01, N10, N11, **kwargs):
        return Fraction(N11,
                        math.sqrt( (N11 + N10) * (N11 + N01) ))

class Minkowski(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return -math.sqrt( Fraction(N10 + N01,
                                    N11 + N10) )

class HubertsGamma(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return Fraction(N11 * N00 - N10 * N01,
                        math.sqrt(
                            (N11 + N10)*(N11 + N01)
                        ) * math.sqrt(
                            (N00 + N10)*(N00 + N01)
                        ))

class AbsHubertsGamma(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return abs(Fraction(N11 * N00 - N10 * N01,
                        math.sqrt(
                            (N11 + N10)*(N11 + N01)
                        ) * math.sqrt(
                            (N00 + N10)*(N00 + N01)
                        )))

class YuleIndex(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return Fraction(N11 * N00 - N10 * N01,
                        N11 * N10 + N00 * N01)

class DiceIndex(PairCountingScore):
    def paircounting_score(N01, N10, N11, **kwargs):
        return Fraction(2 * N11,
                        2 * N11 + N10 + N01)

class KulczynskiIndex(PairCountingScore):
    def paircounting_score(N01, N10, N11, **kwargs):
        return (
            Fraction(N11, N11 + N10)
            + Fraction(N11, N11 + N01)
        ) / 2

class McConnaugheyIndex(PairCountingScore):
    def paircounting_score(N01, N10, N11, **kwargs):
        return Fraction(N11*N11 - N01*N10,
                       (N11 + N10) * (N11 + N01)
        )

class PeirceIndex(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return Fraction(N11*N00 - N01*N10,
                       (N11 + N10) * (N00 + N01)
        )

class SokalAndSneath1(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return (
            Fraction(N11, N11 + N10)
            + Fraction(N11, N11 + N01)
            + Fraction(N00, N00 + N10)
            + Fraction(N00, N00 + N01)
        ) / 4

class Baulieu1(PairCountingScore):
    def paircounting_score(N01, N10, N, **kwargs):
        return (
            N**2
            - N * (N10 + N01)
            + (N10 - N01)**2
        ) / N**2

class SokalAndSneath2(PairCountingScore):
    def paircounting_score(N01, N10, N11, **kwargs):
        return Fraction(N11,
                        N11 + 2*( N10 + N01 ) )

class SokalAndSneath3(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return Fraction(N11 * N00,
                        math.sqrt(
                            (N11 + N10)*(N11 + N01)
                        ) * math.sqrt(
                            (N00 + N10)*(N00 + N01)
                        ))

class GowerAndLegendre(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return (N11 + N00) / (
            N11 + N00 + ( N01 + N10 ) / 2
        )

class RogersAndTanimoto(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return (N11 + N00) / (
            N11 + N00 + 2*( N01 + N10 )
        )

class GoodmanAndKruskal(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return Fraction(N11*N00 - N10*N01,
                        N11*N00 + N10*N01)

class Baulieu2(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, N, **kwargs):
        return (N11 * N00 - N10 * N01) / N**2

class RussellAndRao(PairCountingScore):
    def paircounting_score(N11, N, **kwargs):
        return N11 / N

class FagerAndMcGowan(PairCountingScore):
    def paircounting_score(N01, N10, N11, **kwargs):
        return Fraction(N11 - math.sqrt(N11 + N01) / 2,
                        math.sqrt( (N11 + N10)*(N11 + N01) ))

class AdjustedMirkinMetric(PairCountingScore):
    isdistance = True
    def paircounting_score(N01, N10, N, **kwargs):
        return -2 * ( N10 + N01 ) / float(N)

class PearsonCoefficient(PairCountingScore):
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return Fraction(
            N11 * N00 - N10 * N01,
            math.sqrt(
                (N11 + N10)*(N11 + N01)
            ) * math.sqrt(
                (N00 + N10)*(N00 + N01)
            )) # The sqrt wasn't in the table but seems necessary

class CorrelationDistance(PearsonCoefficient):
    isdistance = True
    def paircounting_score(N00, N01, N10, N11, **kwargs):
        return np.arccos(PearsonCoefficient.paircounting_score(N00, N01, N10, N11, **kwargs))/math.pi

# Standardization under the assumption that N11~Binom(min(mA,mB),max(mA,mB)/N).
class StandardizedRandIndex2(PairCountingScore):
    def paircounting_score(N11, N, paircounts, **kwargs):
        p = max(paircounts.mA, paircounts.mB) / N
        n_trials = min(paircounts.mA, paircounts.mB)
        return Fraction(
            N11 - n_trials*p,
            math.sqrt(
                n_trials*p*(1-p)
            ))

# Standardization under the assumption that N11~Binom(N,mAmB/N^2).
class StandardizedRandIndex1(PairCountingScore):
    def paircounting_score(N11, N, paircounts, **kwargs):
        p = paircounts.mA * paircounts.mB / N**2
        n_trials = N
        return Fraction(
            N11 - n_trials*p,
            math.sqrt(
                n_trials*p*(1-p)
            ))

# Convenient in some cases
class N11(PairCountingScore):
    def paircounting_score(N11, **kwargs):
        return N11

class GeneralizedIndex(PairCountingScore):
    r=1
    c0=0
    c2=1
    @classmethod
    def paircounting_score(cls, N00, N01, N10, N11, N, paircounts, **kwargs):
        r = kwargs['r'] if 'r' in kwargs else cls.r
        c0 = kwargs['c0'] if 'c0' in kwargs else cls.c0
        c2 = kwargs['c2'] if 'c2' in kwargs else cls.c2
        x=N11/N
        pA=x+min(N10,N01)/N
        pB=x+max(N10,N01)/N
        m=GeneralizedMean(Fraction(pA,pB),Fraction(1-pB,1-pA),r=r)
        return c0 + (c2-c0)*m*Fraction(x-pA*pB,pA*(1-pB))

class HarmonicIndex(GeneralizedIndex):
    r = -1

class GeometricIndex(GeneralizedIndex):
    r = 0

class ArithmeticIndex(GeneralizedIndex):
    r = 1
    # To make it equal to Sokal&Sneath1
    c0 = 0.5
    c2 = 1

LeiPairCountingList = [
    RandIndex,
    AdjustedRandIndex,
    MirkinMetric,
    JaccardIndex,
    HubertIndex,
    WallaceIndex,
    FowlkesAndMallowIndex,
    Minkowski,
    HubertsGamma,
    AbsHubertsGamma,
    YuleIndex,
    DiceIndex,
    KulczynskiIndex,
    McConnaugheyIndex,
    PeirceIndex,
    SokalAndSneath1,
    Baulieu1,
    RussellAndRao,
    FagerAndMcGowan,
    PearsonCoefficient,
    Baulieu2,
    SokalAndSneath2,
    SokalAndSneath3,
    GowerAndLegendre,
    RogersAndTanimoto,
    GoodmanAndKruskal
]

NCinc = [
    RandIndex,
    MirkinMetric,
    HubertIndex,
    Minkowski,
    GowerAndLegendre,
    RogersAndTanimoto,
    Baulieu1,
    YuleIndex,
    GoodmanAndKruskal
]
NCnone = [
    AdjustedRandIndex,
    PearsonCoefficient,
    SokalAndSneath1
]
NCdec = [
    Baulieu2,
    PeirceIndex,
    RussellAndRao,
    KulczynskiIndex,
    McConnaugheyIndex,
    JaccardIndex,
    WallaceIndex,
    FowlkesAndMallowIndex,
    DiceIndex,
    FagerAndMcGowan,
    SokalAndSneath2,
    SokalAndSneath3
]

GeneralizedIndices = [
    ArithmeticIndex,
    GeometricIndex,
    HarmonicIndex
]

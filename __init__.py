from .Clustering import Clustering
from . import InformationTheoreticIndices as ITI
from . import PairCountingIndices as PCI
from .FMeasure import FMeasure
from .BCubed import BCubed

Indices = [
    ITI.AvgNMI,
    ITI.MaxNMI,
    ITI.VariationOfInformation,
    ITI.FairNMI,
    PCI.RandIndex,
    PCI.AdjustedRandIndex,
    PCI.JaccardIndex,
    PCI.DiceIndex,
    PCI.WallaceIndex,
    PCI.SokalAndSneath1,
    PCI.PearsonCoefficient,
    PCI.CorrelationDistance,
    FMeasure,
    BCubed
]

NamedIndices = {
    'NMI': ITI.AvgNMI,
    'MaxNMI': ITI.MaxNMI,
    'VI': ITI.VariationOfInformation,
    'FNMI': ITI.FairNMI,
    'Rand': PCI.RandIndex,
    'ARI': PCI.AdjustedRandIndex,
    'Jaccard': PCI.JaccardIndex,
    'Dice': PCI.DiceIndex,
    'Wallace': PCI.WallaceIndex,
    'S&S1': PCI.SokalAndSneath1,
    'CC': PCI.PearsonCoefficient,
    'CD': PCI.CorrelationDistance,
    'FM': FMeasure,
    'BCubed': BCubed
}

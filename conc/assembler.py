import itertools as it
from typing import List, Type

from concepts import ConceptBase, Sent, Ep
from precedents import precedents

ROOT_CONCEPT = Ep

Concepts = List[Type[ConceptBase]]
Concept = Type[ConceptBase]


def assemble(concepts: Concepts):

    Ep(concepts)

    root_concept = None
    for precedents_row in precedents:
        for maybe_root_concept in precedents_row:
            if maybe_root_concept in map(lambda c: type(c), concepts):
                root_concept = type(maybe_root_concept)
                break

    unconsumed_concepts, sub_trees = concepts, []
    for index, concept in enumerate(concepts):
        if type(concept) == root_concept:
            sub_tree = None
            try:
                remaining_concepts, sub_tree = build_tree(root_concept, unconsumed_concepts, index)
            except ValueError as e:
                print(e)
            assert None in remaining_concepts
            sub_trees.append(sub_tree)
            unconsumed_concepts = remaining_concepts


def build_tree(root_concept: Concept, concepts: Concepts, concept_index: int) -> (Concepts, list):
    assert concepts[concept_index] == root_concept
    sub_tree = []
    if hasattr(root_concept, 'populate_children'):
        root_concept.populate_children(concepts, concept_index)
    else:
        return concepts, root_concept



from uuid import uuid4

from py4j.java_gateway import JavaGateway


class ELReasoner:
    def __init__(self, filepath: str) -> None:
        ### INITIALIZATION ###

        # connect to the java gateway of dl4python
        self.gateway = JavaGateway()

        # get a parser from OWL files to DL ontologies
        self.parser = self.gateway.getOWLParser()
        self.ontology = self.parser.parseFile(filepath)

        # get a formatter to print in nice DL format
        self.formatter = self.gateway.getSimpleDLFormatter()

        self.gateway.convertToBinaryConjunctions(self.ontology)

        # get all concepts occurring in the ontology
        self.allConcepts = self.ontology.getSubConcepts()
        self.conceptNames = self.ontology.getConceptNames()

        self.elFactory = self.gateway.getELFactory()

        self.tbox = self.ontology.tbox().getAxioms()

    def check_subsumption(self, subsumer, subsumee) -> bool:
        # This DICTIONARY will have individuals as keys and their SET of concepts as values
        current_interpretation = {"d0": {subsumee}}

        # This will keep the dict of roles and successors for each individual
        successor_dict = {"d0": {}}

        changed = True
        while changed:
            changed = False
            for d in list(current_interpretation.keys()):
                changed |= self.apply_rules(
                    d, current_interpretation, successor_dict, subsumer
                )

        # Check if D was assigned to d
        return subsumer in current_interpretation["d0"]

    def apply_rules(self, d, current_interpretation, successor_dict, subsumer):
        changed = False

        # ⊤-rule: Add ⊤ to any individual.
        top = self.elFactory.getTop()
        if top not in current_interpretation[d]:
            current_interpretation[d].add(top)
            changed = True

        # ⊓-rule 1: If d has C ⊓ D assigned, assign also C and D to d.
        for concept in list(current_interpretation[d]):
            conceptType = concept.getClass().getSimpleName()
            if conceptType == "ConceptConjunction":
                for conjunct in concept.getConjuncts():
                    if conjunct in self.allConcepts:
                        current_interpretation[d].add(conjunct)
                        changed = True

        # ⊓-rule 2: If d has C and D assigned, assign also C ⊓ D to d.
        for c1 in list(current_interpretation[d]):
            for c2 in list(current_interpretation[d]):
                if c1 != c2:
                    conjunct_concept = self.elFactory.getConjunction(c1, c2)
                    if conjunct_concept in self.allConcepts:
                        current_interpretation[d].add(conjunct_concept)
                        changed = True

        # ∃-rule 1: If d has ∃r.C assigned, connect to an existing e with C or create one
        found = False
        for concept in current_interpretation[d]:
            conceptType = concept.getClass().getSimpleName()
            if conceptType == "ExistentialRoleRestriction":
                # check if there is an existing element with C
                for key, value in current_interpretation.items():
                    if self.formatter.format(concept.filler()) in value:
                        successor_dict[d].add({concept.role: {key}})
                        found = True
                        changed = True

                if not (found):
                    uuid = uuid4()
                    current_interpretation[uuid] = {concept.filler()}
                    successor_dict[d][concept.role] = uuid
                    changed = True

        # ∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
        if d in successor_dict:
            for role in successor_dict[d]:
                for successor in successor_dict[d]:
                    if successor in current_interpretation:
                        for concept in current_interpretation[successor]:
                            current_interpretation[d].add(
                                self.elFactory.getExistentialRoleRestriction(
                                    role, concept
                                )
                            )
                            changed = True

        # ⊑-rule: If d has C assigned and C ⊑ D ∈ T, then also assign D to d.
        copy = current_interpretation[d].copy()
        for concept in copy:
            for axiom in self.tbox:
                if axiom.getClass().getSimpleName() == "GeneralConceptInclusion":
                    left = axiom.lhs()
                    right = axiom.rhs()
                    if (
                        left == concept
                        and right in self.allConcepts
                        and right not in current_interpretation[d]
                    ):
                        current_interpretation[d].add(right)
                        changed = True

        for concept in current_interpretation["d0"]:
            if self.formatter.format(concept) == self.formatter.format(subsumer):
                changed = False
                break
        return changed

    def _get_all_subsumers(self, subsumee):
        subsumers = {subsumee}

        for concept in self.conceptNames:
            if concept not in subsumers:
                if self.check_subsumption(concept, subsumee):
                    subsumers.add(concept)

        return subsumers

    def get_all_subsumers(self, subsumee: str):
        return self._get_all_subsumers(self.elFactory.getConceptName(subsumee))

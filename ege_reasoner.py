
### INITIALIZATION ###

from py4j.java_gateway import JavaGateway
import sys
import datetime

# connect to the java gateway of dl4python
gateway = JavaGateway()

# get a parser from OWL files to DL ontologies
parser = gateway.getOWLParser()

# get a formatter to print in nice DL format
formatter = gateway.getSimpleDLFormatter()

# ont_name = sys.argv[1]
# class_name = sys.argv[2]

# ontology = parser.parseFile(ont_name)
ontology = parser.parseFile("burgers.rdf")

gateway.convertToBinaryConjunctions(ontology)

# get all concepts occurring in the ontology
allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()

elFactory = gateway.getELFactory()

tbox = ontology.tbox().getAxioms()


"""
TO DO
- Edit to list all subsumers
- Edit to receive and check input (from cmd)

Notes to self:
- use formatter
"""

def check_subsumption(subsumer, subsumee):
    
    # This DICTIONARY will have individuals as keys and their SET of concepts as values
    current_interpretation = {"d0": {subsumee}}

    # This will keep the dict of roles and successors for each individual
    successor_dict = {"d0" : {}}

    changed = True
    subsumer_found = False
    while changed:
        changed = False
        for d in list(current_interpretation.keys()):
            changed |= apply_rules(d, current_interpretation, successor_dict, subsumer)

    # Check if D was assigned to d
    if subsumer in current_interpretation["d0"]:
        return True
    else:
        return False
    
def apply_rules(d, current_interpretation, successor_dict, subsumer):
    changed = False

    # ⊤-rule: Add ⊤ to any individual.
    top = elFactory.getTop()
    if top not in current_interpretation[d]:
        current_interpretation[d].add(top)
        changed = True

    # ⊓-rule 1: If d has C ⊓ D assigned, assign also C and D to d.
    for concept in list(current_interpretation[d]):
        conceptType = concept.getClass().getSimpleName()
        if conceptType == "ConceptConjunction":
            for conjunct in concept.getConjuncts():
                    if conjunct in allConcepts:
                        current_interpretation[d].add(conjunct)
                        changed = True

    # ⊓-rule 2: If d has C and D assigned, assign also C ⊓ D to d.
    for c1 in list(current_interpretation[d]):
        for c2 in list(current_interpretation[d]):
            if c1 != c2:
                conjunct_concept = elFactory.getConjunction(c1,c2)
                if conjunct_concept in allConcepts:
                    current_interpretation[d].add(conjunct_concept)
                    changed = True

    # ∃-rule 1: If d has ∃r.C assigned, connect to an existing e with C or create one
    found = False
    for concept in current_interpretation[d]:
        conceptType = concept.getClass().getSimpleName()
        if conceptType == "ExistentialRoleRestriction":
            # check if there is an existing element with C 
            for key, value in current_interpretation.items():
                if formatter.format(concept.filler()) in value:
                    successor_dict[d].add({concept.role : {key}})
                    found = True
                    changed = True
            
            if not(found):
                timeID = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                current_interpretation[timeID] = {concept.filler()}
                successor_dict[d][concept.role] = timeID
                changed = True

    # ∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
    if d in successor_dict:
        for role in successor_dict[d]:
            for successor in successor_dict[d]:
                if successor in current_interpretation:
                    for concept in current_interpretation[successor]:
                        current_interpretation[d].add(elFactory.getExistentialRoleRestriction(role, concept))
                        changed = True


    # ⊑-rule: If d has C assigned and C ⊑ D ∈ T, then also assign D to d.
    copy = current_interpretation[d].copy()
    for concept in copy:
        for axiom in tbox:
            if axiom.getClass().getSimpleName() == "GeneralConceptInclusion":
                left = axiom.lhs()
                right = axiom.rhs()
                if left == concept and right in allConcepts and right not in current_interpretation[d]:
                    current_interpretation[d].add(right)
                    changed = True

    for concept in current_interpretation["d0"]:
        if formatter.format(concept) == formatter.format(subsumer):
            changed = False
            break
    return changed


def get_all_subsumers(subsumee):
    subsumers = {subsumee} # subsumers of the input

    ### we dont need this func because it is not recursive anymore
    def find_subsumers(concept): 
        nonlocal subsumers

        if check_subsumption(concept, subsumee): # continue if it is a subsumer of the input
            subsumers.add(concept)

    for concept in conceptNames: # touch all concepts
        if concept not in subsumers: # check if note added to the set
            find_subsumers(concept)

    return subsumers


 
input_subsumer = "VeganFood"
input_subsumee = "Salad"

subsumer_concept = elFactory.getConceptName(input_subsumer)
subsumee_concept = elFactory.getConceptName(input_subsumee)

for c in get_all_subsumers(subsumee_concept):
    print(c)



# result = check_subsumption(subsumer_concept, subsumee_concept)




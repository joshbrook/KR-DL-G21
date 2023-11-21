
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
    while changed:
        changed = False
        for d in list(current_interpretation.keys()):
            changed |= apply_rules(d, current_interpretation, successor_dict)
            for concept in current_interpretation["d0"]:
                print()

    # Check if D was assigned to d
    if subsumer in current_interpretation["d0"]:
        return "YES"
    else:
        return "NO"
    
def apply_rules(d, current_interpretation, successor_dict):
    changed = False

    # ⊤-rule: Add ⊤ to any individual.
    top = elFactory.getTop()
    if top not in current_interpretation[d]:
        current_interpretation[d].add(top)
        changed = True

    # ⊓-rule 1: If d has C ⊓ D assigned, assign also C and D to d.
##### check if the concept we are adding occurs in the tbox (including nested concepts)
    for concept in list(current_interpretation[d]):
        conceptType = concept.getClass().getSimpleName()
        if conceptType == "ConceptConjunction":
            for conjunct in concept.getConjuncts():
                    current_interpretation[d].add(conjunct)
            changed = True
    print('rule 1 complete')

    # ⊓-rule 2: If d has C and D assigned, assign also C ⊓ D to d.
    for c1 in list(current_interpretation[d]):
        for c2 in list(current_interpretation[d]):
            if c1 != c2:
                current_interpretation[d].add(elFactory.getConjunction(c1,c2))
                changed = True
    print('rule 2 complete')

    # ∃-rule 1: If d has ∃r.C assigned, connect to an existing e with C or create one
    found = False
    for concept in current_interpretation[d]:
        conceptType = concept.getClass().getSimpleName()
        if conceptType == "ExistentialRoleRestriction":
            # check if there is an existing element with C 
            for key, value in current_interpretation:
                if concept.filler() in current_interpretation[key]:
                    successor_dict[d].add({concept.role : {key}})
                    found = True
                    changed = True
            
            if not(found):
                timeID = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                current_interpretation[timeID] = {concept.filler()}
                successor_dict[d].add({concept.role : {timeID}})
                changed = True
    print('rule 3 complete')

    # ∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
    for role in successor_dict[d].keys():
        for successor in successor_dict[role]:
            for concept in current_interpretation[successor]:
                current_interpretation[d].add(elFactory.getExistentialRoleRestriction(role, concept))
                changed = True
    print('rule 4 complete')

    # ⊑-rule: If d has C assigned and C ⊑ D ∈ T, then also assign D to d.
    copy = current_interpretation[d].copy()
    for concept in copy:
        print('-----' + formatter.format(concept))
        for axiom in tbox:
            axiomType = axiom.getClass().getSimpleName()
            if axiomType == "GeneralConceptInclusion" and axiom.lhs() == concept:
                current_interpretation[d].add(axiom.rhs())
                changed = True
    print('rule 5 complete')

    return changed

 

 
input_subsumer = '"Meat"'
input_subsumee = '"Beef"'

subsumer_concept = elFactory.getConceptName(input_subsumer)
subsumee_concept = elFactory.getConceptName(input_subsumee)

result = check_subsumption(subsumer_concept, subsumee_concept)
print(f"Result: {result}") # YES or NO




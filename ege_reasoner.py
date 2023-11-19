


"""
TO DO
-/ Initialize start variables and define functions
- How do we compare concept names???
- Figure out how to approach iterating over axioms
- Write the code for each rule one by one
- Edit to list all subsumers
- Edit to receive and check input (from cmd)

Notes to self:
- get methods only create, not fetch. use loops to find the concept

"""

def check_subsumption(subsumer, subsumee):
    
    # This DICTIONARY will have individuals as keys and their SET of concepts as values
    current_interpretation = {initial_individual: {elFactory.getConceptName("subsumee")}}

    changed = True
    while changed:
        changed = False
        for d in list(current_interpretation.keys()):
            changed |= apply_rules(d, current_interpretation)

    # Check if D was assigned to d
    if subsumer in current_interpretation[initial_individual]:
        return "YES"
    else:
        return "NO"
    
def apply_rules(d, current_interpretation):
    changed = False

    # ⊤-rule: Add ⊤ to any individual.
    if top not in current_interpretation[d]:
        current_interpretation[d].add(top)
        changed = True
# TO DO
    # ⊓-rule 1: If d has C ⊓ D assigned, assign also C and D to d.
    for concept in list(current_interpretation[d]):
        if _:
            concepts = _
            current_interpretation[d].update(concepts)
            changed = True

    # ⊓-rule 2: If d has C and D assigned, assign also C ⊓ D to d.
    for c1 in list(current_interpretation[d]):
        for c2 in list(current_interpretation[d]):
            if c1 != c2:
                current_interpretation[d].add(elFactory.getConjunction(c1,c2))
                changed = True
# TO DO
    # ∃-rule 1: If d has ∃r.C assigned
    for concept in list(current_interpretation[d]):
        _
# TO DO
    # ∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
    for role, successors in current_interpretation[d].items():
        for successor in successors:
            concepts = 
            for concept in concepts:
                
# TO DO
    # ⊑-rule: If d has C assigned and C ⊑ D ∈ T, then also assign D to d.
    for concept in list(current_interpretation[d]):
        for axiom in tbox:
            if axiom.getClass().getSimpleName() == "SubClassOf" and axiom. :
                
                changed = True

    return changed


### INITIALIZATION ###

from py4j.java_gateway import JavaGateway

# connect to the java gateway of dl4python
gateway = JavaGateway()

# get a parser from OWL files to DL ontologies
parser = gateway.getOWLParser()

# get a formatter to print in nice DL format
formatter = gateway.getSimpleDLFormatter()

ontology = parser.parseFile("pizza.owl")  # Replace with our ontology file

gateway.convertToBinaryConjunctions(ontology)

# get all concepts occurring in the ontology
allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()

elFactory = gateway.getELFactory()

tbox = ontology.tbox().getAxioms()

initial_individual = "d0"

input_subsumer = "D"
input_subsumee = "C"

result = check_subsumption(input_subsumer, input_subsumee)
print(f"Result: {result}") # YES or NO











# Creating EL concepts and axioms
conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
role = elFactory.getRole("r")
existential = elFactory.getExistentialRoleRestriction(role,conjunctionAB)
top = elFactory.getTop()
conjunction2 = elFactory.getConjunction(top,existential)

gci = elFactory.getGCI(conjunctionAB,conjunction2)
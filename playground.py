from py4j.java_gateway import JavaGateway

# connect to the java gateway of dl4python
gateway = JavaGateway()

# get a parser from OWL files to DL ontologies
parser = gateway.getOWLParser()

# get a formatter to print in nice DL format
formatter = gateway.getSimpleDLFormatter()

# load an ontology from a file
ontology = parser.parseFile("burgers.rdf")

gateway.convertToBinaryConjunctions(ontology)

# get the TBox axioms
tbox = ontology.tbox()
axioms = tbox.getAxioms()

# get all concepts occurring in the ontology
allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()



# Creating EL concepts and axioms

elFactory = gateway.getELFactory()

conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
role = elFactory.getRole("r")
existential = elFactory.getExistentialRoleRestriction(role,conjunctionAB)
top = elFactory.getTop()
conjunction2 = elFactory.getConjunction(top,existential)

gci = elFactory.getGCI(conjunctionAB,conjunction2)


x = elFactory.getConceptName('"CheesyPizza"')
set1 = {x}

for c in [formatter.format(y) for y in conceptNames]:
    if c == x:
        set1.add(c)

print(len(set1))

# EL reasoner group 21

Install (presumably in some virtual environment) before running:

```shell
python -m pip install .
```

To run, first run the JAR:

```shell
java -jar dl4python-0.1-jar-with-dependencies.jar
```

This could be done in python too, but would sadly require too much of a rewrite of the Scala code to get this to work (the sunk costs spent on that are high, tough...)

After this, the reasoner can be run via:

```shell
python -m el_reasoner [ontology_file] [class_name]
```

Or, run the experiment with:

```shell
python experiment.py ontology/burgers.rdf "Salad" "1,2,3,4,5"
```

import os
import csv
import json
import sys
from collections import defaultdict

def get_csv_files(folder):
    csv_files = []
    for root, dirs, files in os.walk(folder, topdown = False):
        for filename in files:
            name, extension = os.path.splitext(filename)
            if extension == ".csv":
                csv_files.append(os.path.join(root, filename))
    return csv_files

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_filename(path):
    head, tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    return name

def get_dirname(path):
    head, tail = os.path.split(path)
    return head.split("/")[-1]

class IDFactory:

    def __init__(self):
        self.n = 0
        self.node_ids = {}

    def get_node_id(self, node_id=None):
        if node_id == None:
            return self.__get_next()
        else:
            if node_id not in self.node_ids:
                self.node_ids[node_id] = self.__get_next()
            return self.node_ids[node_id]
    
    def get_edge_id(self):
        return self.__get_next()

    def __get_next(self):
        self.n = self.n + 1
        return self.n

class Node:
    def __init__(self):
        self.id = None
        self.labels = []
        self.properties = defaultdict(list)

    def set_id(self, _id):
        self.id = _id
        return self

    def add_label(self, value):
        self.labels.append(value)
        return self

    def add_property(self, key, value):
        self.properties[key].append(value)
        return self

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

def node_as_dict(node):
    return {
        "id": node.id,
        "labels": node.labels,
        "properties": node.properties
    }

class Edge:
    def __init__(self):
        self.id = None
        self.source_id = None
        self.target_id = None
        self.labels = []
        self.properties = defaultdict(list)

    def set_id(self, _id):
        self.id = _id
        return self

    def set_source_id(self, value):
        self.source_id = value
        return self

    def set_target_id(self, value):
        self.target_id = value
        return self

    def add_label(self, value):
        self.labels.append(value)
        return self

    def add_property(self, key, value):
        self.properties[key].append(value)
        return self

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

def edge_as_dict(edge):
    return {
        "id": edge.id,
        "from": edge.source_id,
        "to": edge.target_id,
        "labels": edge.labels,
        "properties": edge.properties
    }

class PropertyGraph: 
    def __init__(self):
        self.nodes = set()
        self.edges = set()
    
    def add_node(self, node):
        self.nodes.add(node)
        return self

    def add_edge(self, edge):
        self.edges.add(edge)
        return self

def propery_graph_as_dict(propery_graph):
    return {
        "nodes": list(map(node_as_dict, list(propery_graph.nodes))),
        "edges": list(map(edge_as_dict, list(propery_graph.edges))),
    }

if __name__ == "__main__":
    
    print("Number of arguments:", len(sys.argv), "arguments.")
    print("Argument List:", str(sys.argv))

    if len(sys.argv) != 3:
        print("Please specify input and output folders.")
        exit(1)

    input_folder = sys.argv[1]
    output_base_folder = sys.argv[2]

    print("Input folder: {}".format(input_folder))
    print("Output folder: {}".format(output_base_folder))

    ensure_dir(output_base_folder)

    csv_files = get_csv_files(input_folder)

    print("Progress: {:.2%}".format(0), end="\r", flush=True)

    id_factory = IDFactory()

    for i, csv_file in enumerate(csv_files):

        property_graph = PropertyGraph()

        input_file = open(csv_file, "r")
        reader = csv.DictReader(input_file)
        
        output_folder = os.path.join(output_base_folder, get_dirname(csv_file))
        ensure_dir(output_folder)

        output_filename = os.path.join(output_folder, "{}.json".format(get_filename(csv_file)))

        for row in reader:

            observation_property = row["property"]
            observation_value = row["value"]
            observation_unit = row["unit"]
            sensor_name = row["sensorId"]

            sensor_id = id_factory.get_node_id(sensor_name)
            observation_id= id_factory.get_node_id()
            edge_id = id_factory.get_edge_id()

            sensor_node = Node() \
                .set_id(sensor_id) \
                .add_label("Sensor") \
                .add_property("name", sensor_name)

            observation_node = Node() \
                .set_id(observation_id) \
                .add_label("Observation") \
                .add_property("property", observation_property) \
                .add_property("value", float(observation_value)) \
                .add_property("unit_of_measure", observation_unit)

            sensor_observation_edge = Edge() \
                .set_id(edge_id) \
                .set_source_id(sensor_id) \
                .set_target_id(observation_id) \
                .add_label("HAS_OBSERVED")

            property_graph \
                .add_node(sensor_node) \
                .add_node(observation_node) \
                .add_edge(sensor_observation_edge)

        input_file.close()

        output_file = open(output_filename, "w")
        output_file.write(json.dumps(propery_graph_as_dict(property_graph),separators=(',', ':')))
        output_file.close()

        print("Progress: {:.2%}".format(i / len(csv_files)), end="\r", flush=True)
    
    print("Progress: {:.2%}".format(1), flush=True)

    print("Done!")
    

  
# SRBench

This repository contains the CSV data of [SRBench](https://www.w3.org/wiki/SRBench) [1]

## Download
Check out the release section to download the latest dataset version.
Two different serializations are available:
- CSV: the folder structure resembles the original data format.
```
charley/
└── extracted/
    ├── sensor_X/
    │   └── AirTemperature/
    │       └──file.csv
    ├── sensor_Y/
    └── sensor_Z/
```
- JSON-PG [2]: the data is organized in JSON files. Each file is named with a UNIX timestamp and contains the JSON-PG serialization of the events that occurred at the specified time instant.
```
charley/
└── pg-json/
    ├── 1091923500.json
    └── 1091923800.json
```

## Build
To generate JSON-PG representation:

- Build docker image:
```
docker build -t json-pg .
```
- Run the docker image mounting the input and output volumes as follows:
```
docker run \
    -v ${PWD}/input/charley:/data/input \
    -v ${PWD}/output/charley:/data/output \
    json-pg
```
- The output folder contains the PG-JSON representation of the data.

## References

[1] Zhang Y., Duc P.M., Corcho O., Calbimonte JP. (2012) SRBench: A Streaming RDF/SPARQL Benchmark. In: Cudré-Mauroux P. et al. (eds) The Semantic Web – ISWC 2012. ISWC 2012. Lecture Notes in Computer Science, vol 7649. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-35176-1_40

[2] Chiba, H., Yamanaka, R. and Matsumoto, S., 2019. Property Graph Exchange Format. arXiv preprint https://arxiv.org/abs/1907.03936.

# JSON schemas for Bioconductor objects

## Overview

This repository contains JSON schemas for saving Bioconductor objects to file using a language-agnostic format.
Each schema generally corresponds to a single Bioconductor class and contains the metadata required to restore that object in memory.
We use both schema-based composition and inheritance to capture complex object classes and their BioC inheritance hierarchy.
The aim is to portably save and read BioC objects in different language ecosystems like R (obviously), Python and Javascript.

## Contents

See the [Pages sites](https://artifactdb.github.io/BiocObjectSchemas) for a link to all available schemas.
Developers may also download the bundle of the latest schemas [here](https://artifactdb.github.io/BiocObjectSchemas/bundle.tar.gz).

See [`docs/schema_conventions.md`](docs/schema_conventions.md) for instructions on writing new schemas.

See [`docs/elastic_search_mapping.md`](docs/elastic_search_mapping.md) for converting schemas into Elasticsearch mappings.

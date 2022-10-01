# JSON schemas for Bioconductor objects

## Overview

This repository contains JSON schemas for saving Bioconductor objects to file using a language-agnostic format.
Each schema generally corresponds to a single Bioconductor class and contains the metadata required to restore that object in memory.
We use both schema-based composition and inheritance to capture complex object classes and their BioC inheritance hierarchy.
The aim is to portably save and read BioC objects in different language ecosystems like R (obviously), Python and Javascript.

## Contents

See the [Pages site](https://artifactdb.github.io/BiocObjectSchemas) for all available schemas in human-readable form.

Check the [Releases page](https://github.com/ArtifactDB/BiocObjectSchemas/releases) for versioned releases of the schemas.

See [`docs/schema_conventions.md`](docs/schema_conventions.md) for instructions on writing new schemas.

See [`docs/elastic_search_mapping.md`](docs/elastic_search_mapping.md) for converting schemas into Elasticsearch mappings.

## Schema customization 

To customize these schemas, simply [fork](https://github.com/ArtifactDB/BiocObjectSchemas/fork) this repository and modify the schemas in `raw/`.
The GitHub Action will then validate and build the resolved schemas for use in downstream applications.

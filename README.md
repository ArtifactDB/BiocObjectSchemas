# JSON schemas for Bioconductor objects

## Overview

This repository contains JSON schemas for saving Bioconductor objects to file using a language-agnostic format.
Each schema generally corresponds to a single Bioconductor class and contains the metadata required to restore that object in memory.
We use both schema-based composition and inheritance to capture complex object classes and their BioC inheritance hierarchy.
The aim is to portably save and read BioC objects in different language ecosystems like R (obviously), Python and Javascript.

## Contents

The [`raw`](raw) subdirectory contains the raw JSON schemas, prior to resolution of `$ref`s.

See the [Pages site](https://artifactdb.github.io/BiocObjectSchemas) for all available schemas in human-readable form.

Check the [Releases page](https://github.com/ArtifactDB/BiocObjectSchemas/releases) for versioned releases of the resolved schemas.

See [`docs/schema_conventions.md`](docs/schema_conventions.md) for instructions on writing new schemas.

See [`docs/elastic_search_mapping.md`](docs/elastic_search_mapping.md) for converting schemas into Elasticsearch mappings.

## Schema customization 

To customize these schemas, we suggest the following set-up:

```sh
mkdir custom-schemas
cd custom-schemas

# Adding this repository as a submodule.
git init
git submodule add https://github.com/ArtifactDB/BiocObjectSchemas original

# Making our own raw subdirectory with softlinks to the originals.
mkdir raw
cd raw
for x in $(ls ../original/raw) 
do
    ln -s ../original/raw/$x $x
done
git add raw

# Copying the GitHub action.
cp -r original/.github .
git add .github
```

A schema can then be customized by removing the corresponding softlink and replacing it with a real directory with a `v*.json` file.
This new file will then be used in place of the original when resolving `$ref`-based references in the [GitHub Action](.github/workflows/build.yaml).
The most obvious method for creating a new file is to just copy one of the original files and apply the modifications.
For example, we could add an author field to the `_common` subschema:

```json
{
    "additionalProperties": false,
    "properties": {
        "$schema": {
            "type": "string",
            "description": "The schema to use."
        },
        "path": {
            "type": "string",
            "description": "Path to the file in the project directory."
        },
        "is_child": {
            "type": "boolean",
            "description": "Is this a child document, only to be interpreted in the context of the parent document from which it is linked? This may have implications for search and metadata requirements.",
            "default": false
        },
        "authors": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "Names of the authors."
            }
        }
    },
    "required": [
        "$schema",
        "path"
    ]
}
```

A more elegant approach is to build on top of the original by creating a `$ref` to the submodule.
This is used to add more properties on top of an existing data structure, guaranteeing compatibility with downstream tools that operate on the original schema. 
For example, to add an extra `FOO` property onto the `summarized_experiment` schema:

```json
{
    "allOf": [ { "$ref": "../../original/raw/summarized_experiment/v1.json" } ],
    "properties": {
        "summarized_experiment": {
            "type": "object",
            "properties": {
                "FOO": {
                    "type": "integer",
                    "description": "Yet another property"
                }
            }
        }

    }
}
```

And of course, it is possible to create entirely new schemas altogether.

# Schema writing conventions

## Naming

Snake case is expected for all properties and directory names.

Schema files should be named `<TYPE>/<VERSION>.json`.
`<VERSION>` should be formatted as `v<NUMBER>`.

## Scoping

Most properties specific to a schema should be scoped inside an object with the same name as the schema's directory.
For example, for a schema in `scoped/v1.json`, we would expect:

```json
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "scoped/v1.json",
    "type": "object",
    "title": "blah",
    "description": "I am a good example of a scoped schema.",
    "required": [
        "scoped"
    ],
    "properties": {
        "scoped": {
            "type": "object",
            "required": [
                "prop1"
            ],
            "properties": {
                "prop1": {
                    "type": "string",
                    "description": "First property"
                },
                "prop2": {
                    "type": "string",
                    "description": "Second property"
                }
            }
        }
    }
}
```

The above is preferred over the direct specification of those properties in the schema's `properties`.
For example, the following is not desirable:

```json
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "unscoped/v1.json",
    "type": "object",
    "title": "blah",
    "description": "I am a bad example of an unscoped schema.",
    "required": [
        "prop1"
    ],
    "properties": {
        "prop1": {
            "type": "string",
            "description": "First property"
        },
        "prop2": {
            "type": "string",
            "description": "Second property"
        }
    }
}
```

We prefer the former as it avoids potential conflicts between different schemas that define the same `prop1` property.
Such conflicts will cause problems during schema inheritance and for the Elasticsearch field mapping.

## Resource pointers

Pointers to other resources should have a `resource` object in its properties.
In the example below, the third property is a pointer to another resource; this pulls in the [`_resource` schema](_resource/v1.json) (assuming we are inside a `BLAH/` directory at this point).

```json
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "BLAH/v1.json",
    "type": "object",
    "title": "blah",
    "description": "I am a blah.",
    "required": [
        "BLAH"
    ],
    "properties": {
        "BLAH": {
            "type": "object",
            "required": [
                "prop1"
            ],
            "properties": {
                "prop1": {
                    "type": "string",
                    "description": "First property"
                },
                "prop2": {
                    "type": "string",
                    "description": "Second property"
                },
                "prop3": {
                    "type": "object",
                    "description": "Pointer to something",
                    "allOf": [ { "$ref": "../_resource/v1.json" } ]
                }
            }
        }
    }
}
```

The `_resource` schema provides the reserved `resource` property, which indicates that a schema may potentially refer to other resources.
This can be helpful for further programming on the schema, e.g., to automatically merging metadata documents.
However, it also means that developers should not use `resource` properties in other contexts.

Developers can hint at the expected type of resource that is referenced by `resource.path`, by inserting a `_children` tag into the `resource` object.
This should contain the names (with or without qualifying versions) of the schemas of the expected resources, which can be used for extra validation.
In the example below, the resource defined by `prop3` may be any version of genomic ranges or version 1 of a genomic ranges list.

```json
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "BLAH/v1.json",
    "type": "object",
    "title": "blah",
    "description": "I am a blah.",
    "required": [
        "BLAH"
    ],
    "properties": {
        "BLAH": {
            "type": "object",
            "required": [
                "prop3"
            ],
            "properties": {
                "prop3": {
                    "type": "object",
                    "description": "Pointer to something",
                    "allOf": [ { "$ref": "../_resource/v1.json" } ],
                    "properties": {
                        "resource": {
                            "_children": {
                                "contains": ["genomic_ranges", "genomic_ranges_list/v1.json"]
                            }
                        }
                    }
                }
            }
        }
    }
}
```

## Mimicking inheritance

We mimic inheritance (in the object-orientated sense of the word) from one schema to a more specialized schema by using `allOf` and `$ref` statements.
This requires any document to validate against the specified parent schema as well as the current schema.
For example, we could "inherit" from `summarized_experiment/v1.json` with the following:

```json
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "special_summarized_experiment/v1.json",
    "type": "object",
    "title": "Special summarized experiment",
    "description": "blah blah balh",
    "allOf": [ { "$ref": "../summarized_experiment/v1.json" }]

    "required": [ "special_summarized_experiment" ],
    "properties": {
        "special_summarized_experiment": {
            "type": "object",
            "properties": {}
        }
    }
}
```

Note that we should have a scoped `special_summarized_experiment` property, _even if we don't have any additional properties to add!_
This allows us to capture the schema hierarchy inside each document so that interfaces can operate on different levels of specialization.
For example, if we subsequently inherited from this schema, we would still have a `special_summarized_experiment` property in the document to indicate that the resource could be interpreted as a `special_summarized_experiment`.

The [`single_cell_experiment` schema](single_cell_experiment/v1.json) is a good example of this mechanism.
It re-uses content from the [`summarized_experiment` schema](summarized_experiment/v1.json) while still defining its own single-cell-specific properties.

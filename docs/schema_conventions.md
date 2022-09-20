# Schema writing conventions

# Minimal properties

All schemas should follow the [JSON schema standard](https://json-schema.org/).

The `title` and `description` properties should be present.
These should be strings providing an informative title and description of the artifact.

The `properties` should define the `$schema`, `path` and `is_child` properties.
this is most easily done by including one of the [`_common` subschemas](../raw/_common/v1.json) in an `allOf`.

For schemas that do not define pure metadata artifacts, the `properties` should contain the `md5sum` property.
This is most easily done by including one of the [`_md5sum` subschemas](../raw/_md5sum/v1.json) in an `allOf`.

## Naming

Snake case is expected for all properties and directory names.

Schema files should be named `<TYPE>/<VERSION>.json`.
`<VERSION>` should be formatted as `v<NUMBER>`, e.g., the `data_frame` schema would look like `data_frame/v2.json`.

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
    "allOf": [ { "$ref": "../raw/_common/v1.json" } ],
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
    "allOf": [ { "$ref": "../raw/_common/v1.json" } ],
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

For each schema, all scoped properties should be non-empty in every JSON document based on that schema.
This ensures that scoped properties are not inadvertently removed by certain processing tools (e.g., Elasticsearch).
The presence of a scoped property is still informative even if it contains no data, see [below](#mimicking-inheritance) for details.

## Resource pointers

Pointers to other resources should have a `resource` object in its properties.
In the example below, the third property is a pointer to another resource; this pulls in the [`_resource` subschema](../raw/_resource/v1.json) (assuming we are inside a `BLAH/` directory at this point).

```json
{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "BLAH/v1.json",
    "type": "object",
    "title": "blah",
    "description": "I am a blah.",
    "allOf": [ { "$ref": "../raw/_common/v1.json" } ],
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
Specifically, `_children.contains` is a string array that specifies all of the allowable types that can be used as a child in that part of the schema.
The example below requires a `genomic_ranges` or `genomic_ranges_list` resource for `prop3`.

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
                                "contains": ["genomic_ranges", "genomic_ranges_list"]
                            }
                        }
                    }
                }
            }
        }
    }
}
```

This mark-up allows schema-traversing tools to easily determine what can or cannot be used as a child of a particular artifact.
Note that "subclasses" of the listed types are also allowed (see the [next section](#mimicking-inheritance) for details),
so a resource based on a different schema may be legal as long as `genomic_ranges` or `genomic_ranges_list` is present in the properties of the child object's metadata.

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
            "properties": {
                "BLAH": {
                    "type": "string",
                    "description": "Explanation of why I am special..."
                }
            }
        }
    }
}
```

The key here is the presence of a scoped `special_summarized_experiment` property.
This allows us to capture the schema hierarchy inside each document so that interfaces can operate on different levels of specialization.
Applications can still interpret a `special_summarized_experiment`-based metadata document as a `summarized_experiment` by reading its `summarized_experiment` property, 
even if the application doesn't understand how to deal with the `special_summarized_experiment` specialization.
For this reason, it is important to ensure that the scoped properties are always non-empty.
This ensures that these properties are not accidentally removed during processing, as their presence is still informative even though they lack any content.

The [`single_cell_experiment` schema](single_cell_experiment/v1.json) is a good example of this mechanism.
It re-uses content from the [`summarized_experiment` schema](summarized_experiment/v1.json) while still defining its own single-cell-specific properties.

## Defining attributes

Developers may define an `_attributes` field at the top level of their schemas.
This should be a JSON object and may contain any number of these fields:

- `restore`, a JSON object containing restoration commands for one of more languages.
  For R, we expect a string containing a namespaced function that will be called by `alabaster.base::loadObject()`.
  This attribute is used by the _alabaster.\*_ framework to determine how to load artifacts back into an R session.
- `metadata_only`, a boolean indicating whether this schema describes a metadata-only artifact.
  If `true`, the `path` should point to the JSON metadata file rather than another file.
  This attribute is used by the _alabaster.\*_ framework to determine whether MD5 checksums need to be computed/validated.
  Defaults to `false` if not specified.
- `format`, a string containing the expected MIME type for artifacts of this type.
  This is largely ceremonial.

For example, the schema below tells us that we need to use `alabaster.blah::loadBlah` to obtain an R object from this artifact.

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
                }
            }
        }
    },
    "_attributes": {
        "restore": {
            "R": "alabaster.blah::loadBlah"
        }
    }
}
```

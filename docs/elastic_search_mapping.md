# Defining Elasticsearch mappings

## Overview

JSON schemas can, with some effort, be converted into Elasticsearch mappings.
This allows us to store the metadata documents in an Elasticsearch index for rapid search and retrieval.
Unfortunately, this conversion is not unambiguous as JSON schema data types can correspond to multiple Elasticsearch field data types.
For example, a JSON `string` type can be mapped to Elasticsearch `text` or `keyword` types.

To facilitate automatic conversion, schema authors need to insert some instructions about the appropriate field type for each property in the schema.
This involves adding an extra `_elasticsearch` field in the definition of each property, for example:

```json
{
   "properties": {
        "some_property": {
            "type": "string",
            "description": "I am a property",
            "_elasticsearch": {
                "type": "keyword"
            }
        }
    }
}
```

The `_elasticsearch.type` value specifies the Elasticsearch field type for the enclosing property.
In addition, we can also specify:

- `_elasticsearch.index`, a boolean that indicates whether to index a particular property for searching.
This defaults to `true` but can be set to `false` for certain fields that only need to be stored in Elasticsearch.
Reducing the number of indexed fields can improve the performance of Elasticsearch.

The rest of this document will describe the default interpretation and possible alternatives for each JSON schema data type.

## `string`

### As a keyword (default)

For JSON `string` types, the default interpretation is the Elasticsearch `keyword` field type.
This is best used for structured content like identifiers and enables aggregations and sorting on the field, at the cost of not being able to search for individual words inside the string.

If this interpretation is desired, no `_elasticsearch` field is necessary, though one can explicitly state it:

```json
{
   "properties": {
        "some_property": {
            "type": "string",
            "description": "I am a property",
            "_elasticsearch": {
                "type": "keyword"
            }
        }
    }
}
```

### As text

The other common alternative is that of an Elasticsearch `text`.
This will instruct Elasticsearch to run the string through an analyzer to break it up into individual items (e.g., words).
Each item is then indexed to enable searching on words within the string.

```json
{
   "properties": {
        "some_property": {
            "type": "string",
            "description": "I am a property",
            "_elasticsearch": {
                "type": "text"
            }
        }
    }
}
```

## `integer`

### As 32-bit integers (default)

For JSON `integer` types, the default interpretation is the Elasticsearch `integer` field type. 
This defines a 32-bit signed integer with a minimum value of -2147483648 and a maximum value of 2147483647.

If this interpretation is desired, no `_elasticsearch` field is necessary, though one can explicitly state it:

```json
{
   "properties": {
        "some_property": {
            "type": "integer",
            "description": "I am a property",
            "_elasticsearch": {
                "type": "integer"
            }
        }
    }
}
```

### As 16-bit integers

For smaller integers, we can instead use a 16-bit signed integer with a minimum value of -32768 and a maximum value of 32767.
This can save some memory and is best used for non-data-related values, e.g., version numbers.

```json
{
   "properties": {
        "some_property": {
            "type": "integer",
            "description": "I am a property",
            "_elasticsearch": {
                "type": "short"
            }
        }
    }
}
```

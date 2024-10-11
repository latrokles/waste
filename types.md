# types

like the usual types...

- `nil` for nil...
- booleans `t` and `f`.
- integers `1`, `-50`, `1_000`
- floating point values `3.141592`
- strings `'hello'`...
  - mutable vs. immutable ...
- lists `[ 1 2 3 4 ]` (no commas...)
- hash `{{ :key1 val1 :key2 val2 :key3 val3 }}`
- objects `{:type :slot-name slot-value}`
- functions (TBD)

maybe some convenience things like...

- keywords `:foo`
- datetime and date literals like [frink](https://frinklang.org/#DateTimeHandling) ??

few other things to consider:

- single line comments
- multiline comments
- variable / parameter metadata
- docstrings?

## functions

some things to consider around functions...

- implicit parameter/arguments (ie. tacit or point free programming)
- explicit parameter/arguments
  - how to identify or delimit them
    - a list like lisp?
    - a map
    - implicit
- delimiting the body of a function
  - parens a la lisp
  - leading blank space like python or haskell
  - curly braces or similar
    - backwards curly braces `def inc x } return x + 1 {` ROFL...
  - enclosing words, `def/do/begin... end` 
- implicit v. explicit returns...
- expressions v. statements...



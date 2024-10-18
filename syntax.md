# Syntax

**Symbols**
Used for identifiers, they have a namespace, a name, and metadata. They can contain alphanumeric characters and `*`, `+`, `!`, `?`, `_`, `_`, `<`, `>`, `=`. `event-handler`, `str>int`, `empty?`, `update!` are all valid symbols.

**Literals**
- Strings: enclosed in single quotes `'hello world'`, they are immutable.
- Integers: `10`, `1_000`.
- Floats: `3.1459`, `5_000.50`.
- Nil: `nil`, the absence of a value.
- Booleans: `t` and `f`.
- Keywords: 

**Tagged Literals / Data Literals**
- builtins
  - datetime
  - date
  - ?
- custom defined

**Lists**
Collection of objects enclosed in `#[ ]`. `#[ 1 2 3 4 ]`. No commas required.

**Maps**
Value pairs enclosed in `#{ }` like `#{ :x 10 :y 20 }`.

**Functions**

**Control Flow**
- conditionals
  - if
  - when
  - unless
  - cond

- iteration
  - foreach
  - while
  - until
  - times
  - loop

**Records and runtime polymorphism**

Records
Multimethods
Methods

**Metadata**





defining an anonymous function

```
[ x y | + x y ]
```

calling an anonymous function
```
[ x y | + x y ] 10 5  ; should return 15
```

conditionals:
```
if expr if-true-fn if-false-fn

when expr fn
unless expr fn
```

iteration:
```
map fn collection
foreach fn collection
while test-expr fn
until test-expr fn
times N fn
repeat fn
```

definitions:
```
defun
defmulti
defmethod
defrecord
derive
```

### some additional stuff...

- Maybe container...
```
or-value (maybe nil) 4  ; returns 4
```

- threading / compose ...
```
(->> #[ 'car', 'cat', 'bar' ] 
     (map [ x | upcase x ] _) 
     (filter [ x | starts-with? 'c' ] _))
```

- namespaces and use/import...
```
namespace :my-namespace
use :some-namespace
use :other-namespace/some-symbol
```

- code storage / image / codebase
- persistent records
  - eavt storage

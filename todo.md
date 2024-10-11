# todo 

I kinda like [factor](https://factorcode.org)'s use of `IN`, `USING`, `USE`.

```
IN: waste.tools.todo
USING: waste/std/time
USING: waste/std/uuid
```

Now one could use a symbol from that module(?) prefixed by the module name:

```
time/now
```


```
defrecord Todo [ :uid :description :state :created-on :completed-on ]

defm complete [ todo::Todo ]
  set-slot todo :state :DONE .
  set-slot todo :completed-on (time/now) .
  ^todo .
;

def make-todo [ description ]
  ^Todo*{ (uuid/uuid4) description :PENDING (time/now) nil } .
```

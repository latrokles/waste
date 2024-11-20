# what-if lisp

```
(namespace :tools/todo)
(use :idutils)
(use :datetime)

(defobj Todo [:uid :title :status :created-on :updated-on])

(defn make-todo [title]
  (->Todo (:idutils/uuid4)
          title
		  'OPEN'
		  (:datetime/local-now)
		  nil))

(defn list-todos []
  (list-instances Todo))

(defn query-todos [query-dict]
 (filter #() (list-todos)))

(defmethod complete [(Todo todo)]
  (status<< todo 'DONE')
  (updated-on<< todo :datetime/now-local))
```

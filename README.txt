@Author --> Jacob Wilson

last edit: 11:42pm June 24th

examples

1) Data structure
The data structure for a LIST expression is not the standard Python list we are used to.
We use a structure borrowed from the implementation of functional programming languages
such as LISP that stores the first item (referred to as the car) and a list of remaining
items (referred to as cdr) in a Python list in a recursive manner as shown in the examples above.
Also note that we go ahead and execute the "cons" operation while constructing the data structure itself.
  LISP Expression
    Python List
    34
    ['num',34]
    x
    ['var','x']
    (+ (* 2 x) 9)
    ['+',['*',['num',2],['var','x']],['num',9]]
    (car (2 3))
    ['car', [['num', 2.0], [['num', 3.0], []]]]
    (let ((x 2)(y 4)) (+ x y))
    ['let', [['x', ['num', 2.0]], ['y', ['num', 4.0]]], ['+', ['var', 'x'], ['var', 'y']]]

  LIST Expression
    (1 2 x 4)
    [['num', 1.0], [['num', 2.0], [['var', 'x'], [['num', 4.0], []]]]]
    (2 4 (+ 2 4) 8)
    [['num', 2.0], [['num', 4.0], [['+', ['num', 2.0], ['num', 4.0]], [['num', 8.0], []]]]]
    (1 (car (2 3)) 4)
    [['num', 1.0], [['car', [['num', 2.0], [['num', 3.0], []]]], [['num', 4.0], []]]]
    (cdr (10 20 30))
    ['cdr', [['num', 10.0], [['num', 20.0], [['num', 30.0], []]]]]
    (cons 2 (cdr (10 20 30)))
    [['num', 2.0], ['cdr', [['num', 10.0], [['num', 20.0], [['num', 30.0], []]]]]]
2) Sample run
    LISP: 34;

    The value is 34.0

    LISP: (+ 20 30);

    The value is 50.0

    LISP: (/ 9 (- 2 2));

    EVALUATION ERROR: Divide by 0!

    LISP: (* (+ 1 2) (/ 8 4));

    The value is 6.0

    LISP: (* (car (2 4 (+ 2 4) 8)) (/ 27 9));

    The value is 6.0

    LISP: (+ (car (2 3 4)) (car (cdr (cdr (9 8 7 6)))));

    The value is 9.0

    LISP: (+ 2 3 4);

    SYNTAX ERROR

    LISP: (* (car 4) 22);

    SYNTAX ERROR

    LISP: (+ 3 (car (cdr (cdr (cdr (1 2))))));

    CDR of empty list Error!

    LISP: (cdr (1 2 3 4));

    The value is (2.0 3.0 4.0)

    LISP: (cdr (cons (+ 2 3) (4 5 6)));

    The value is (4.0 5.0 6.0)

    LISP: (cdr (cdr (1 2 3 4)));

    The value is (3.0 4.0)

    LISP: (cdr (cdr (3 4)));

    The value is ()

    LISP: (cdr (cdr (3)));

    CDR of empty list Error!

    LISP: (let ((x 10) (y (+ 25 (car (20 30)))) (z (+ 10 23)))  (+ x (car (y 20 z))) );

    The value is 55.0

    LISP: (let ((x 2)(y 3)) (+ (* x 4) (*y 3)));

    The value is 17.0

    LISP: (let ((x 2)(y 3)) (+ (* x 4) (* z 3)));

    EVALUATION ERROR: Uninstantiated Variable z

    LISP: (let ((x 2)(y 3)) (let ((x 10)(z 20)) (+ x (+ y z))));

    The value is 33.0

    LISP: (car (cdr (cdr (1 2))));

    Cannot evaluate CAR of EMPTY List!

    LISP: exit;

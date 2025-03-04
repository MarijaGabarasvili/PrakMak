# Test 1: Full tree


## Generating GameTree(5)
generation took 0.000945 seconds, it`s size:
65 nodes, 14 KB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 4            | 4             |
| 2     | 12           | 9             |
| 3     | 24           | 12            |
| 4     | 24           | 10            |

### Nodes at Level 3
| Sequence        | P1 Score | P2 Score |
|----------------|----------|----------|
| 00               | 0        | -1       |
| 00               | 0        | 1        |
| 00               | 0        | 1        |
| 01               | 0        | 1        |
| 01               | 0        | 1        |
| 01               | 2        | -1       |
| 10               | -2       | -1       |
| 10               | -2       | -1       |
| 10               | -2       | -1       |
| 10               | -2       | -1       |
| 10               | -2       | -1       |
| 10               | -2       | 1        |
| 10               | 0        | 1        |
| 10               | 0        | 1        |
| 10               | 2        | -1       |
| 11               | -2       | -1       |
| 11               | -2       | -1       |
| 11               | -2       | -1       |
| 11               | -2       | 1        |
| 11               | -2       | 1        |
| 11               | 0        | -1       |
| 11               | 0        | -1       |
| 11               | 0        | -1       |
| 11               | 2        | 1        |
```
└── Seq: 10010 | Score (P1:P2): 0:0 |
    ├── Seq: 1010 | Score (P1:P2): -1:0 |
    │   ├── Seq: 110 | Score (P1:P2): -1:-1 |
    │   │   ├── Seq: 00 | Score (P1:P2): 0:-1 |
    │   │   │   └── Seq: 1 | Score (P1:P2): 0:0 |
    │   │   └── Seq: 11 | Score (P1:P2): -2:-1 |
    │   │       └── Seq: 0 | Score (P1:P2): -2:0 |
    │   ├── Seq: 100 | Score (P1:P2): -1:-1 |
    │   │   ├── Seq: 10 | Score (P1:P2): -2:-1 |
    │   │   │   └── Seq: 1 | Score (P1:P2): -2:-2 |
    │   │   └── Seq: 11 | Score (P1:P2): 0:-1 |
    │   │       └── Seq: 0 | Score (P1:P2): 0:0 |
    │   └── Seq: 101 | Score (P1:P2): -1:-1 |
    │       ├── Seq: 11 | Score (P1:P2): -2:-1 |
    │       │   └── Seq: 0 | Score (P1:P2): -2:0 |
    │       └── Seq: 10 | Score (P1:P2): -2:-1 |
    │           └── Seq: 1 | Score (P1:P2): -2:-2 |
    ├── Seq: 1110 | Score (P1:P2): 1:0 |
    │   ├── Seq: 010 | Score (P1:P2): 1:1 |
    │   │   ├── Seq: 00 | Score (P1:P2): 0:1 |
    │   │   │   └── Seq: 1 | Score (P1:P2): 0:2 |
    │   │   └── Seq: 01 | Score (P1:P2): 0:1 |
    │   │       └── Seq: 0 | Score (P1:P2): 0:0 |
    │   ├── Seq: 100 | Score (P1:P2): 1:1 |
    │   │   ├── Seq: 10 | Score (P1:P2): 0:1 |
    │   │   │   └── Seq: 1 | Score (P1:P2): 0:0 |
    │   │   └── Seq: 11 | Score (P1:P2): 2:1 |
    │   │       └── Seq: 0 | Score (P1:P2): 2:2 |
    │   └── Seq: 111 | Score (P1:P2): 1:-1 |
    │       ├── Seq: 01 | Score (P1:P2): 2:-1 |
    │       │   └── Seq: 0 | Score (P1:P2): 2:-2 |
    │       └── Seq: 10 | Score (P1:P2): 2:-1 |
    │           └── Seq: 1 | Score (P1:P2): 2:-2 |
    ├── Seq: 1000 | Score (P1:P2): -1:0 |
    │   ├── Seq: 100 | Score (P1:P2): -1:-1 |
    │   │   ├── Seq: 10 | Score (P1:P2): -2:-1 |
    │   │   │   └── Seq: 1 | Score (P1:P2): -2:-2 |
    │   │   └── Seq: 11 | Score (P1:P2): 0:-1 |
    │   │       └── Seq: 0 | Score (P1:P2): 0:0 |
    │   ├── Seq: 110 | Score (P1:P2): -1:1 |
    │   │   ├── Seq: 00 | Score (P1:P2): 0:1 |
    │   │   │   └── Seq: 1 | Score (P1:P2): 0:2 |
    │   │   └── Seq: 11 | Score (P1:P2): -2:1 |
    │   │       └── Seq: 0 | Score (P1:P2): -2:2 |
    │   └── Seq: 101 | Score (P1:P2): -1:1 |
    │       ├── Seq: 11 | Score (P1:P2): -2:1 |
    │       │   └── Seq: 0 | Score (P1:P2): -2:2 |
    │       └── Seq: 10 | Score (P1:P2): -2:1 |
    │           └── Seq: 1 | Score (P1:P2): -2:0 |
    └── Seq: 1001 | Score (P1:P2): -1:0 |
        ├── Seq: 101 | Score (P1:P2): -1:-1 |
        │   ├── Seq: 11 | Score (P1:P2): -2:-1 |
        │   │   └── Seq: 0 | Score (P1:P2): -2:0 |
        │   └── Seq: 10 | Score (P1:P2): -2:-1 |
        │       └── Seq: 1 | Score (P1:P2): -2:-2 |
        ├── Seq: 111 | Score (P1:P2): -1:1 |
        │   ├── Seq: 01 | Score (P1:P2): 0:1 |
        │   │   └── Seq: 0 | Score (P1:P2): 0:0 |
        │   └── Seq: 10 | Score (P1:P2): 0:1 |
        │       └── Seq: 1 | Score (P1:P2): 0:0 |
        └── Seq: 100 | Score (P1:P2): -1:-1 |
            ├── Seq: 10 | Score (P1:P2): -2:-1 |
            │   └── Seq: 1 | Score (P1:P2): -2:-2 |
            └── Seq: 11 | Score (P1:P2): 0:-1 |
                └── Seq: 0 | Score (P1:P2): 0:0 |
```

# Test 2: Tree size


## Generating GameTree(5)
generation took 0.001001 seconds, it`s size:
65 nodes, 14 KB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 4            | 4             |
| 2     | 12           | 8             |
| 3     | 24           | 10            |
| 4     | 24           | 8             |


## Generating GameTree(7)
generation took 0.003611 seconds, it`s size:
1 957 nodes, 439 KB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 6            | 6             |
| 2     | 30           | 20            |
| 3     | 120          | 40            |
| 4     | 360          | 48            |
| 5     | 720          | 37            |
| 6     | 720          | 27            |


## Generating GameTree(9)
generation took 0.241387 seconds, it`s size:
109 601 nodes, 23 MB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 8            | 8             |
| 2     | 56           | 38            |
| 3     | 336          | 91            |
| 4     | 1,680        | 151           |
| 5     | 6,720        | 150           |
| 6     | 20,160       | 112           |
| 7     | 40,320       | 71            |
| 8     | 40,320       | 46            |


## Generating GameTree(11)
generation took 31.990873 seconds, it`s size:
9 864 101 nodes, 2 GB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 10           | 10            |
| 2     | 90           | 66            |
| 3     | 720          | 213           |
| 4     | 5,040        | 439           |
| 5     | 30,240       | 525           |
| 6     | 151,200      | 433           |
| 7     | 604,800      | 287           |
| 8     | 1,814,400    | 183           |
| 9     | 3,628,800    | 112           |
| 10    | 3,628,800    | 67            |

# Test 4: Random moves by picking first number of the two to merge


## Generating GameTree(15) 
Generation took 0.608353 seconds

Move #: 0 | Player: 1 | Sequence: 111101101000011 | Score: 0:0 |
266 645 nodes, 58 MB


# Randomly traversing until reaching a terminal state...


Picked 11 and 12, move 1 took 0.470499992371 s, next move:
Move #: 1 | Player: 2 | Sequence: 11110110100111 | Score: 1:0 | 
173 487 nodes, 37 MB

Picked 12 and 13, move 2 took 0.244991779327 s, next move:
Move #: 2 | Player: 1 | Sequence: 1111011010010 | Score: 1:1 | 
108 387 nodes, 23 MB

Picked 5 and 6, move 3 took 0.144301414490 s, next move:
Move #: 3 | Player: 2 | Sequence: 111100010010 | Score: 2:1 | 
64 475 nodes, 13 MB

Picked 9 and 10, move 4 took 0.076993227005 s, next move:
Move #: 4 | Player: 1 | Sequence: 11110001000 | Score: 2:0 | 
36 105 nodes, 7 MB

Picked 2 and 3, move 5 took 0.033859729767 s, next move:
Move #: 5 | Player: 2 | Sequence: 1100001000 | Score: 3:0 | 
18 735 nodes, 4 MB

Picked 1 and 2, move 6 took 0.017996788025 s, next move:
Move #: 6 | Player: 1 | Sequence: 110001000 | Score: 3:-1 |
8 807 nodes, 1 MB

Picked 5 and 6, move 7 took 0.009063005447 s, next move:
Move #: 7 | Player: 2 | Sequence: 11000100 | Score: 2:-1 |
3 627 nodes, 787 KB

Picked 6 and 7, move 8 took 0.001996517181 s, next move:
Move #: 8 | Player: 1 | Sequence: 1100011 | Score: 2:0 |
1 245 nodes, 271 KB

Picked 4 and 5, move 9 took 0.000989913940 s, next move:
Move #: 9 | Player: 2 | Sequence: 110001 | Score: 1:0 |
335 nodes, 74 KB

Picked 4 and 5, move 10 took 0.000000000000 s, next move:
Move #: 10 | Player: 1 | Sequence: 11000 | Score: 1:-1 |
75 nodes, 16 KB

Picked 2 and 3, move 11 took 0.000000000000 s, next move:
Move #: 11 | Player: 2 | Sequence: 1110 | Score: 2:-1 |
27 nodes, 5 KB

Picked 1 and 2, move 12 took 0.000000000000 s, next move:
Move #: 12 | Player: 1 | Sequence: 100 | Score: 2:0 |
17 nodes, 3 KB

Picked 1 and 2, move 13 took 0.000000000000 s, next move:
Move #: 13 | Player: 2 | Sequence: 11 | Score: 3:0 |
15 nodes, 3 KB

Picked 0 and 1, move 14 took 0.000000000000 s, next move:
Move #: 14 | Player: 1 | Sequence: 0 | Score: 3:1 |
15 nodes, 3 KB

```
Game ended. Final tree structure from root:
└── Seq: 111101101000011 | Score (P1:P2): 0:0 |
    └── Seq: 11110110100111 | Score (P1:P2): 1:0 |
        └── Seq: 1111011010010 | Score (P1:P2): 1:1 |
            └── Seq: 111100010010 | Score (P1:P2): 2:1 |
                └── Seq: 11110001000 | Score (P1:P2): 2:0 |
                    └── Seq: 1100001000 | Score (P1:P2): 3:0 |
                        └── Seq: 110001000 | Score (P1:P2): 3:-1 |
                            └── Seq: 11000100 | Score (P1:P2): 2:-1 |
                                └── Seq: 1100011 | Score (P1:P2): 2:0 |
                                    └── Seq: 110001 | Score (P1:P2): 1:0 |
                                        └── Seq: 11000 | Score (P1:P2): 1:-1 |
                                            └── Seq: 1110 | Score (P1:P2): 2:-1 |
                                                └── Seq: 100 | Score (P1:P2): 2:0 |
                                                    └── Seq: 11 | Score (P1:P2): 3:0 |
                                                        └── Seq: 0 | Score (P1:P2): 3:1 |
```
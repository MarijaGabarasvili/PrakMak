# Generating GameTree(5)
generation took 0.000993 seconds, it`s size:
65 nodes, 16 KB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 4            | 4             |
| 2     | 12           | 9             |
| 3     | 24           | 11            |
| 4     | 24           | 10            |

### Nodes at Level 3
| Sequence        | P1 Score | P2 Score |
|----------------|----------|----------|
| 00               | -2       | -1       |
| 00               | -2       | -1       |
| 00               | 0        | 1        |
| 00               | 0        | 1        |
| 00               | 0        | 1        |
| 00               | 0        | 1        |
| 01               | 0        | -1       |
| 01               | 0        | 1        |
| 01               | 0        | 1        |
| 01               | 0        | 1        |
| 01               | 0        | 1        |
| 01               | 2        | -1       |
| 10               | 0        | -1       |
| 10               | 0        | 1        |
| 10               | 0        | 1        |
| 10               | 0        | 1        |
| 10               | 0        | 1        |
| 10               | 2        | -1       |
| 11               | -2       | 1        |
| 11               | 0        | -1       |
| 11               | 0        | -1       |
| 11               | 2        | 1        |
| 11               | 2        | 1        |
| 11               | 2        | 1        |
```
└── Sequence: [0, 0, 1, 1, 0] | Scores: P1=0, P2=0 | Current Player: 1
    ├── Sequence: [1, 1, 1, 0] | Scores: P1=1, P2=0 | Current Player: 2
    │   ├── Sequence: [0, 1, 0] | Scores: P1=1, P2=1 | Current Player: 1
    │   │   ├── Sequence: [0, 0] | Scores: P1=0, P2=1 | Current Player: 2
    │   │   │   └── Sequence: [1] | Scores: P1=0, P2=2 | Current Player: 1
    │   │   └── Sequence: [0, 1] | Scores: P1=0, P2=1 | Current Player: 2
    │   │       └── Sequence: [0] | Scores: P1=0, P2=0 | Current Player: 1
    │   ├── Sequence: [1, 0, 0] | Scores: P1=1, P2=1 | Current Player: 1
    │   │   ├── Sequence: [1, 0] | Scores: P1=0, P2=1 | Current Player: 2
    │   │   │   └── Sequence: [1] | Scores: P1=0, P2=0 | Current Player: 1
    │   │   └── Sequence: [1, 1] | Scores: P1=2, P2=1 | Current Player: 2
    │   │       └── Sequence: [0] | Scores: P1=2, P2=2 | Current Player: 1
    │   └── Sequence: [1, 1, 1] | Scores: P1=1, P2=-1 | Current Player: 1
    │       ├── Sequence: [0, 1] | Scores: P1=2, P2=-1 | Current Player: 2
    │       │   └── Sequence: [0] | Scores: P1=2, P2=-2 | Current Player: 1
    │       └── Sequence: [1, 0] | Scores: P1=2, P2=-1 | Current Player: 2
    │           └── Sequence: [1] | Scores: P1=2, P2=-2 | Current Player: 1
    ├── Sequence: [0, 0, 1, 0] | Scores: P1=-1, P2=0 | Current Player: 2
    │   ├── Sequence: [1, 1, 0] | Scores: P1=-1, P2=1 | Current Player: 1
    │   │   ├── Sequence: [0, 0] | Scores: P1=0, P2=1 | Current Player: 2
    │   │   │   └── Sequence: [1] | Scores: P1=0, P2=2 | Current Player: 1
    │   │   └── Sequence: [1, 1] | Scores: P1=-2, P2=1 | Current Player: 2
    │   │       └── Sequence: [0] | Scores: P1=-2, P2=2 | Current Player: 1
    │   ├── Sequence: [0, 0, 0] | Scores: P1=-1, P2=-1 | Current Player: 1
    │   │   ├── Sequence: [1, 0] | Scores: P1=0, P2=-1 | Current Player: 2
    │   │   │   └── Sequence: [1] | Scores: P1=0, P2=-2 | Current Player: 1
    │   │   └── Sequence: [0, 1] | Scores: P1=0, P2=-1 | Current Player: 2
    │   │       └── Sequence: [0] | Scores: P1=0, P2=-2 | Current Player: 1
    │   └── Sequence: [0, 0, 1] | Scores: P1=-1, P2=-1 | Current Player: 1
    │       ├── Sequence: [1, 1] | Scores: P1=0, P2=-1 | Current Player: 2
    │       │   └── Sequence: [0] | Scores: P1=0, P2=0 | Current Player: 1
    │       └── Sequence: [0, 0] | Scores: P1=-2, P2=-1 | Current Player: 2
    │           └── Sequence: [1] | Scores: P1=-2, P2=0 | Current Player: 1
    ├── Sequence: [0, 0, 0, 0] | Scores: P1=1, P2=0 | Current Player: 2
    │   ├── Sequence: [1, 0, 0] | Scores: P1=1, P2=1 | Current Player: 1
    │   │   ├── Sequence: [1, 0] | Scores: P1=0, P2=1 | Current Player: 2
    │   │   │   └── Sequence: [1] | Scores: P1=0, P2=0 | Current Player: 1
    │   │   └── Sequence: [1, 1] | Scores: P1=2, P2=1 | Current Player: 2
    │   │       └── Sequence: [0] | Scores: P1=2, P2=2 | Current Player: 1
    │   ├── Sequence: [0, 1, 0] | Scores: P1=1, P2=1 | Current Player: 1
    │   │   ├── Sequence: [0, 0] | Scores: P1=0, P2=1 | Current Player: 2
    │   │   │   └── Sequence: [1] | Scores: P1=0, P2=2 | Current Player: 1
    │   │   └── Sequence: [0, 1] | Scores: P1=0, P2=1 | Current Player: 2
    │   │       └── Sequence: [0] | Scores: P1=0, P2=0 | Current Player: 1
    │   └── Sequence: [0, 0, 1] | Scores: P1=1, P2=1 | Current Player: 1
    │       ├── Sequence: [1, 1] | Scores: P1=2, P2=1 | Current Player: 2
    │       │   └── Sequence: [0] | Scores: P1=2, P2=2 | Current Player: 1
    │       └── Sequence: [0, 0] | Scores: P1=0, P2=1 | Current Player: 2
    │           └── Sequence: [1] | Scores: P1=0, P2=2 | Current Player: 1
    └── Sequence: [0, 0, 1, 1] | Scores: P1=-1, P2=0 | Current Player: 2
        ├── Sequence: [1, 1, 1] | Scores: P1=-1, P2=1 | Current Player: 1
        │   ├── Sequence: [0, 1] | Scores: P1=0, P2=1 | Current Player: 2
        │   │   └── Sequence: [0] | Scores: P1=0, P2=0 | Current Player: 1
        │   └── Sequence: [1, 0] | Scores: P1=0, P2=1 | Current Player: 2
        │       └── Sequence: [1] | Scores: P1=0, P2=0 | Current Player: 1
        ├── Sequence: [0, 0, 1] | Scores: P1=-1, P2=-1 | Current Player: 1
        │   ├── Sequence: [1, 1] | Scores: P1=0, P2=-1 | Current Player: 2
        │   │   └── Sequence: [0] | Scores: P1=0, P2=0 | Current Player: 1
        │   └── Sequence: [0, 0] | Scores: P1=-2, P2=-1 | Current Player: 2
        │       └── Sequence: [1] | Scores: P1=-2, P2=0 | Current Player: 1
        └── Sequence: [0, 0, 0] | Scores: P1=-1, P2=1 | Current Player: 1
            ├── Sequence: [1, 0] | Scores: P1=0, P2=1 | Current Player: 2
            │   └── Sequence: [1] | Scores: P1=0, P2=0 | Current Player: 1
            └── Sequence: [0, 1] | Scores: P1=0, P2=1 | Current Player: 2
                └── Sequence: [0] | Scores: P1=0, P2=0 | Current Player: 1

```


# Generating GameTree(7)
generation took 0.004998 seconds, it`s size:
1 957 nodes, 493 KB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 6            | 6             |
| 2     | 30           | 21            |
| 3     | 120          | 37            |
| 4     | 360          | 44            |
| 5     | 720          | 38            |
| 6     | 720          | 27            |


# Generating GameTree(9)
generation took 0.391841 seconds, it`s size:
109 601 nodes, 26 MB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 8            | 8             |
| 2     | 56           | 39            |
| 3     | 336          | 92            |
| 4     | 1,680        | 148           |
| 5     | 6,720        | 148           |
| 6     | 20,160       | 113           |
| 7     | 40,320       | 73            |
| 8     | 40,320       | 46            |


# Generating GameTree(11)
generation took 42.324309 seconds, it`s size:
9 864 101 nodes, 2 GB


### Node Count per Level
| Level | Total States | Unique States |
|-------|--------------|---------------|
| 0     | 1            | 1             |
| 1     | 10           | 10            |
| 2     | 90           | 64            |
| 3     | 720          | 203           |
| 4     | 5,040        | 412           |
| 5     | 30,240       | 500           |
| 6     | 151,200      | 442           |
| 7     | 604,800      | 290           |
| 8     | 1,814,400    | 186           |
| 9     | 3,628,800    | 112           |
| 10    | 3,628,800    | 69            |
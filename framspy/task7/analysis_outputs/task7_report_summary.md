# Task 7 run summary

| Approach | Mean | Median | Stddev | Min | Max | Runs > 1 | Mean completed generations |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1. F1 endpoint | 3.1260 | 0.9225 | 3.5794 | 0.0038 | 8.4689 | 5 | 74.1 |
| 2. F1 endpoint + oscillators | 2.1621 | 0.0038 | 3.3432 | 0.0038 | 8.1708 | 3 | 66.8 |
| 3. F1 sustained | 1.2704 | 1.7173 | 0.8270 | 0.1485 | 2.1905 | 6 | 84.0 |
| 4. F1 lower drift penalties | 1.4703 | 1.7453 | 0.5774 | 0.3235 | 2.0165 | 8 | 166.6 |
| Final F1 | 1.6230 | 1.7495 | 0.3157 | 1.0262 | 1.9373 | 10 | 156.7 |
| Final F4 | 0.6786 | 0.4138 | 0.6806 | 0.0036 | 1.9509 | 3 | 165.6 |

The per-run rows below show best-generation timing and stagnation behavior.

| Approach | Run | Best generation | Best fitness | Completed generations | Improvements | Trailing generations |
|---|---:|---:|---:|---:|---:|---:|
| 1. F1 endpoint | 0 | 80 | 8.4689 | 100 | 34 | 20 |
| 1. F1 endpoint | 1 | 110 | 7.7318 | 130 | 35 | 20 |
| 1. F1 endpoint | 2 | 86 | 5.2121 | 106 | 49 | 20 |
| 1. F1 endpoint | 3 | 14 | 0.0038 | 34 | 3 | 20 |
| 1. F1 endpoint | 4 | 16 | 0.0038 | 36 | 2 | 20 |
| 1. F1 endpoint | 5 | 90 | 1.8382 | 110 | 54 | 20 |
| 1. F1 endpoint | 6 | 7 | 0.0068 | 27 | 4 | 20 |
| 1. F1 endpoint | 7 | 13 | 0.0038 | 33 | 4 | 20 |
| 1. F1 endpoint | 8 | 38 | 0.0038 | 58 | 14 | 20 |
| 1. F1 endpoint | 9 | 87 | 7.9871 | 107 | 29 | 20 |
| 2. F1 endpoint + oscillators | 0 | 49 | 8.0837 | 69 | 25 | 20 |
| 2. F1 endpoint + oscillators | 1 | 10 | 0.0038 | 30 | 7 | 20 |
| 2. F1 endpoint + oscillators | 2 | 16 | 0.0038 | 36 | 2 | 20 |
| 2. F1 endpoint + oscillators | 3 | 37 | 0.0038 | 57 | 14 | 20 |
| 2. F1 endpoint + oscillators | 4 | 17 | 0.0038 | 37 | 9 | 20 |
| 2. F1 endpoint + oscillators | 5 | 141 | 8.1708 | 161 | 50 | 20 |
| 2. F1 endpoint + oscillators | 6 | 67 | 5.1342 | 87 | 49 | 20 |
| 2. F1 endpoint + oscillators | 7 | 21 | 0.2089 | 41 | 13 | 20 |
| 2. F1 endpoint + oscillators | 8 | 67 | 0.0038 | 87 | 15 | 20 |
| 2. F1 endpoint + oscillators | 9 | 43 | 0.0038 | 63 | 12 | 20 |
| 3. F1 sustained | 0 | 39 | 1.7549 | 59 | 16 | 20 |
| 3. F1 sustained | 1 | 80 | 0.2478 | 100 | 18 | 20 |
| 3. F1 sustained | 2 | 42 | 1.6796 | 62 | 17 | 20 |
| 3. F1 sustained | 3 | 94 | 1.8452 | 114 | 26 | 20 |
| 3. F1 sustained | 4 | 90 | 1.9967 | 110 | 29 | 20 |
| 3. F1 sustained | 5 | 34 | 2.1905 | 54 | 9 | 20 |
| 3. F1 sustained | 6 | 60 | 0.1485 | 80 | 23 | 20 |
| 3. F1 sustained | 7 | 91 | 0.4927 | 111 | 35 | 20 |
| 3. F1 sustained | 8 | 97 | 2.1242 | 117 | 37 | 20 |
| 3. F1 sustained | 9 | 13 | 0.2240 | 33 | 7 | 20 |
| 4. F1 lower drift penalties | 0 | 94 | 1.8290 | 144 | 27 | 50 |
| 4. F1 lower drift penalties | 1 | 81 | 1.8033 | 131 | 19 | 50 |
| 4. F1 lower drift penalties | 2 | 81 | 2.0165 | 131 | 24 | 50 |
| 4. F1 lower drift penalties | 3 | 160 | 1.8060 | 200 | 43 | 40 |
| 4. F1 lower drift penalties | 4 | 107 | 1.6873 | 157 | 39 | 50 |
| 4. F1 lower drift penalties | 5 | 193 | 0.4074 | 200 | 70 | 7 |
| 4. F1 lower drift penalties | 6 | 174 | 1.8841 | 200 | 29 | 26 |
| 4. F1 lower drift penalties | 7 | 53 | 1.5728 | 103 | 21 | 50 |
| 4. F1 lower drift penalties | 8 | 198 | 1.3728 | 200 | 62 | 2 |
| 4. F1 lower drift penalties | 9 | 196 | 0.3235 | 200 | 79 | 4 |
| Final F1 | 0 | 146 | 1.7165 | 196 | 65 | 50 |
| Final F1 | 1 | 133 | 1.0455 | 183 | 39 | 50 |
| Final F1 | 2 | 131 | 1.8190 | 181 | 37 | 50 |
| Final F1 | 3 | 58 | 1.9373 | 108 | 31 | 50 |
| Final F1 | 4 | 81 | 1.7826 | 131 | 33 | 50 |
| Final F1 | 5 | 130 | 1.5055 | 180 | 35 | 50 |
| Final F1 | 6 | 108 | 1.9125 | 158 | 28 | 50 |
| Final F1 | 7 | 76 | 1.6748 | 126 | 45 | 50 |
| Final F1 | 8 | 183 | 1.0262 | 200 | 83 | 17 |
| Final F1 | 9 | 54 | 1.8105 | 104 | 35 | 50 |
| Final F4 | 0 | 200 | 0.8076 | 200 | 89 | 0 |
| Final F4 | 1 | 123 | 0.4689 | 173 | 31 | 50 |
| Final F4 | 2 | 194 | 1.4904 | 200 | 70 | 6 |
| Final F4 | 3 | 200 | 0.1053 | 200 | 86 | 0 |
| Final F4 | 4 | 176 | 1.4781 | 200 | 72 | 24 |
| Final F4 | 5 | 74 | 1.9509 | 124 | 45 | 50 |
| Final F4 | 6 | 66 | 0.0036 | 116 | 24 | 50 |
| Final F4 | 7 | 172 | 0.3587 | 200 | 61 | 28 |
| Final F4 | 8 | 49 | 0.1131 | 99 | 33 | 50 |
| Final F4 | 9 | 94 | 0.0089 | 144 | 28 | 50 |

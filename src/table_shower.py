import json
import sys

algorithms = ['Reactive Agent']

table_format = {
    'sizes': [5, 10],
    'prob_total': [0.2, 0.4, 0.6, 0.8],
    'sub_probs': [
        'High Obstacle',
        'High Pit',
        'High Wumpus',
        'Equal',
        'No Obstacle',
        'No Pit',
        'No Wumpus'
    ]
}

entry_order = [
    'turns',
    'score',
    'pit_deaths',
    'wumpus_deaths',
    'shots',
    'kills'
]

def pm(stat):
    return "{0:.2f} +/- ".format(stat[0]) + "{0:.2f}".format(stat[1])


table_data = json.load(open(sys.argv[1]))

for algorithm in algorithms:
    rows = []
    for size in table_format['sizes']:
        row = []
        for prob_total in table_format['prob_total']:
            prob = []
            for split in table_format['sub_probs']:
                prob.append(
                    table_data[str(size)][str(prob_total)][split][algorithm]
                )
            row.append(prob)
        rows.append(row)
    print algorithm
    for row_num, row in enumerate(rows):
        print str(table_format['sizes'][row_num]) + ':: ' + ''.join('['+', '.join(str(i['finished%']) for i in p)+']' for p in row)
        for stat in entry_order:
            print "{}: {}".format(
                stat,
                ''.join('['+', '.join(pm(i[stat]) for i in p)+']' for p in row)
            )


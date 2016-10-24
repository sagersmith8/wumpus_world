import json
import sys

algorithms = ['Reactive Agent']

table_format = {
    'sizes': [5, 10, 15, 20, 25],
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
    return "$"+"{0:.2f} \\pm ".format(stat[0]) + "{0:.2f}".format(stat[1])+"$"


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

        
    print ('\\subsection{'+algorithm+' Results}\n')
    for row_num, row in enumerate(rows):
        print ('\\begin{table}[ht]\n\\centering\n\\resizebox{\\textwidth}{!}{\\begin{tabular}{c|c|c|c|c|c|c|c|c|}\n\\cline{2-9}\n & prob & HO & HP & HW & EQ & NO & NP & NW \\\\\n\\hline\n\\multirow{4}{*}{percent completed}')
        print ('&' + '& '.join(str(table_format['prob_total'][pindex])+' & ' + ' & '.join(str(i['finished%']) for i in p)+'\\\\\n' for pindex, p in enumerate(row))+'\n\\hline')
        
        for stat in entry_order:
            print ('\multirow{4}{*}{' + stat.replace('_',' ') + '}&' +'\\\\\n& '.join(str(table_format['prob_total'][pindex]) + ' & ' + ' & '.join(pm(i[stat]) for i in p)+'' for pindex, p in enumerate(row))+'\\\\\n\\hline\n')
        print('\\end{tabular}}\n\\caption{' + algorithm + ': size ' + str((row_num+1)*5) + '}\n\\end{table}\n\n')


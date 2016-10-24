import logging
import json
import sys

from environment import Environment
import generate_world

import actions
import cell_types

import reactive_agent
import reasoning_agent

algorithms = [
    {
        'name': 'Reactive Agent',
        'run': reactive_agent.run
    }
]
""",
    {
        'name': 'Reasoning Agent',
        'run': reasoning_agent.run
    }]"""

table_format = {
    'sizes': [5, 10, 15, 20, 25],
    'num_worlds': 100,
    'runs_per_world': 1,
    'prob_total': [0.8],
    'sub_probs': [
        ([2, 1, 1], 'High Obstacle'),
        ([1, 2, 1], 'High Pit'),
        ([1, 1, 2], 'High Wumpus'),
        ([1, 1, 1], 'Equal'),
        ([0, 1, 1], 'No Obstacle'),
        ([1, 0, 1], 'No Pit'),
        ([1, 1, 0], 'No Wumpus')
    ]
}

def extract_data(env):
    return {
        'finished': env.finished,
        'score': env.score,        
        'turns': env.turn,
        'pit_deaths': len([1 for death in env.deaths if death[2] == cell_types.PIT]),
        'wumpus_deaths': len([1 for death in env.deaths if death[2] == cell_types.WUMPUS]),
        'kills': len(env.kills),
        'shots': env.action_counts[actions.SHOOT]
    }

def analyze_data(data_list):
    n = len(data_list)
    res = {
        'sample_size': n,
        'finished': 0,
        'finished%': 0
    }
    mean_std_res = {
        'score': [0, 0],
        'turns': [0, 0],
        'pit_deaths': [0, 0],
        'wumpus_deaths': [0, 0],
        'kills': [0, 0],
        'shots': [0, 0]
    }

    for datum in data_list:
        if datum['finished']:
            res['finished'] += 1

    res['finished%'] = res['finished'] / float(n) * 100


    for key in mean_std_res:    
        for datum in data_list:
            mean_std_res[key][0] += datum[key]
        mean_std_res[key][0] /= float(n)
        for datum in data_list:
            mean_std_res[key][1] += (datum[key] - mean_std_res[key][0])**2
        mean_std_res[key][1] /= float(n - 1)            
        mean_std_res[key][1] **= 0.5
        mean_std_res[key][1] /= n ** 0.5
        mean_std_res[key][1] *= 2        

    #for key in mean_std_res:
    #res[key+'_all'] = [datum[key] for datum in data_list]
        
    res.update(mean_std_res)
    return res

fake_logger = logging.getLogger('None')

out_table = {}
for size in table_format['sizes']:
    out_table[size] = {}
    for prob_total in table_format['prob_total']:
        out_table[size][prob_total] = {}
        for split, split_name  in table_format['sub_probs']:
            out_table[size][prob_total][split_name] = {}
            
            total_ratio = sum(split)
            probs = [prob_total * sub_ratio / float(total_ratio)
                     for sub_ratio in split]
            prob_obst, prob_pit, prob_wump = probs
            print prob_obst, prob_pit, prob_wump, split_name
            
            run_data = {}
            for algorithm in algorithms:
                run_data[algorithm['name']] = []
            
            for world_num in xrange(table_format['num_worlds']):
                new_world = generate_world.generate_world(
                    size, prob_obst, prob_pit, prob_wump
                )
                #print '\n'.join(''.join(map(str, row)) for row in new_world.board)
                
                for algorithm in algorithms:
                    for rep in xrange(table_format['runs_per_world']):
                        env = Environment(new_world)
                        print "Run {} on world {} of size {} ({}={}) for algorithm {}".format(rep, world_num, size, split_name, prob_total, algorithm['name'])
                        algorithm['run'](env, fake_logger)
                        run_data[algorithm['name']].append(extract_data(env))

            for algorithm, data in run_data.iteritems():
                out_table[size][prob_total][split_name][algorithm] = analyze_data(data)

json.dump(out_table, open(sys.argv[1], 'w'), indent=4)

                    

import percepts
import navigation


class reactive_agent:



    
    def run(env, position):
        x, y = position
        visited = set()
        safe = set()
        questionable = set()
        actions_to_do = list()
        def is_safe(x, y):
            if (x, y) in safe:
                return True
            return False
        
        navigator = navigation(is_safe())
        
        while not env.is_finished():
            percept = env.get_percepts()

            if not actions_to_do:
                if not percept:
                    #safe = safe + adj_squares()
                elif percepts.GLITTER in percept:
                    env.grab()
                elif percepts.BREEZE in percept or percepts.STENCH in percept:
                    #add adj squares not in safe to questionable
                elif safe:
                    dest = pop(safe)
                    actions_to_do.append(navigator.path_to(relative_pos+direction, dest))
                elif questionable:
                    dest = pop(questionable)
                    actions_to_do.append(navigator.path_to(relative_pos+direction, dest))
            else:
                #do action
                next_action = action_to_do.popleft()
                if next_action == actions.FORWARD:
                    

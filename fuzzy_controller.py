import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


#input universes
horizontal = ctrl.Antecedent(np.arange(-100, 101, 1), 'horizontal')

horizontal['left'] = fuzz.trimf(horizontal.universe, [-100, -100, 0])
horizontal['center'] = fuzz.trimf(horizontal.universe, [-50, 0, 50])
horizontal['right'] = fuzz.trimf(horizontal.universe, [0, 100, 100])

# vertical = ctrl.Antecedent(np.arange(-100, 101, 1), 'vertical')
#
# vertical['down'] = fuzz.trimf(vertical.universe, [-100, -100, 0])
# vertical['center'] = fuzz.trimf(vertical.universe, [-50, 0, 50])
# vertical['up'] = fuzz.trimf(vertical.universe, [0, 100, 100])

#output universe

signal = ctrl.Consequent(np.arange(0, 7, 1), 'signal') # [forward 1, right 3, left 5]

signal['left'] = fuzz.trimf(signal.universe, [1, 1, 1])
signal['forward'] = fuzz.trimf(signal.universe, [2, 2, 2])
signal['right'] = fuzz.trimf(signal.universe, [3, 3, 3])

# horizontal.view()
# vertical.view()
# signal.view()
# input("")

#rules
rule1 = ctrl.Rule(antecedent=horizontal['center'],
                  consequent=signal['forward'])

rule2 = ctrl.Rule(antecedent=horizontal['left'],
                  consequent=signal['left'])

rule3 = ctrl.Rule(antecedent=horizontal['right'],
                  consequent=signal['right'])

# rule1.view()
# input("")


bot_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])


def get_action(h,v):
    instance = ctrl.ControlSystemSimulation(bot_ctrl)
    instance.input['horizontal'] = h
    #instance.input['vertical'] = v
    instance.compute()
    return instance.output['signal']

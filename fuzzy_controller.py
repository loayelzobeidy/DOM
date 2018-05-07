import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


#input universes
horizontal = ctrl.Antecedent(np.arange(-100, 101, 1), 'horizontal')

horizontal['left'] = fuzz.trimf(horizontal.universe, [-100, -100, 0])
horizontal['center'] = fuzz.trimf(horizontal.universe, [-50, 0, 50])
horizontal['right'] = fuzz.trimf(horizontal.universe, [0, 100, 100])


line = ctrl.Antecedent(np.arange(0, 10, 1), 'line')

line['left'] = fuzz.trimf(line.universe, [1, 1, 1])
line['center'] = fuzz.trimf(line.universe, [2, 2, 2])
line['right'] = fuzz.trimf(line.universe, [3, 3, 3])
line['yes'] = fuzz.trapmf(line.universe, [0, 1, 5, 6])
line['no'] = fuzz.trimf(line.universe, [7, 7, 7])
line['3ard'] = fuzz.trimf(line.universe, [5, 5, 5])


#output universe
signal = ctrl.Consequent(np.arange(0, 5, 1), 'signal') # [forward 1, right 3, left 5]

signal['left'] = fuzz.trimf(signal.universe, [1, 1, 1])
signal['forward'] = fuzz.trimf(signal.universe, [2, 2, 2])
signal['right'] = fuzz.trimf(signal.universe, [3, 3, 3])

# horizontal.view()
# line.view()
# signal.view()
# input("")


#rules
rule1 = ctrl.Rule(antecedent=(
                    (horizontal['center'] & line['no']) |
                    (line['center'] & line['yes'])
                  ),
                  consequent=signal['forward'])

rule2 = ctrl.Rule(antecedent=(
                    (horizontal['left'] & line['no']) |
                    (line['left'] & line['yes'])
                  ),
                  consequent=signal['left'])

rule3 = ctrl.Rule(antecedent=(
                    (horizontal['right'] & line['no']) |
                    (line['right'] & line['yes'])      |
                    line['3ard']
                  ),
                  consequent=signal['right'])


bot_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])


def get_action(h, l):
    instance = ctrl.ControlSystemSimulation(bot_ctrl)
    instance.input['horizontal'] = h
    instance.input['line'] = l
    instance.compute()
    return instance.output['signal']


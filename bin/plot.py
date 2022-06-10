#!/usr/bin/env python

# load libraries
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os
import re
import yaml

# Get dictionary of CPU data from benchmark results.
def get_cpu_dict(config, data):
  """Get dictionary of CPU data from benchmark results."""

  # load fields, build result
  rows = data['lscpu']['lscpu']
  r = {row['field'].lower().rstrip(':'): row['data'] for row in rows}

  # get names
  names = None
  if 'names' in config['plot']:
    names = config['plot']['names']

  # add "arch" key
  arch = r['architecture']
  r['arch'] = arch
  if (names is not None) and (arch in names['arches']):
    r['arch'] = names['arches'][arch]

  # add "model" key
  model = r['model name']
  r['model'] = model
  if (names is not None) and (model in names['models']):
    r['model'] = names['models'][model]

  return r

# build path to config.yaml
CONFIG_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'config.yaml')

# read config.yaml
CONFIG = yaml.safe_load(open(CONFIG_PATH))

# read JSON-formatted benchmark data from standard input
DATA = json.load(sys.stdin)

# get x axis tick label locations
x = np.arange(len(DATA['results']))
width = 0.8  # total width of each set

fig, ax = plt.subplots()
bw = width / len(CONFIG['plot']['buffer_sizes'])
for i, row in enumerate(CONFIG['plot']['buffer_sizes']):
  xs = x + (i - len(CONFIG['plot']['buffer_sizes']) / 2 + 0.5) * bw
  ys = [s['data'][i] for s in DATA['results']]
  rect = ax.bar(xs, ys, bw, label = row['name'], color = row['color'])

  # add labels for start and end data points
  if i == 0 or i == len(CONFIG['plot']['buffer_sizes']) - 1:
    ax.bar_label(rect)

# set tick labels
ax.set_xticks(x, [s['name'] for s in DATA['results']])

# get cpu details
cpu_dict = get_cpu_dict(CONFIG, DATA)

# build/set plot title
title = CONFIG['plot']['title'].format_map(cpu_dict)
ax.set_title(title)

# set axis labels
ax.set_xlabel(CONFIG['plot']['x_label'])
ax.set_ylabel(CONFIG['plot']['y_label'])

# set legend
ax.legend(
  title = CONFIG['plot']['legend']['title'],
  loc = CONFIG['plot']['legend']['loc'],
)

# set output dimensions (inches)
out_size = CONFIG['plot']['output_size']
fig.set_size_inches(out_size[0], out_size[1])

plt.show()

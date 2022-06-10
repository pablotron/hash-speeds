#!/usr/bin/env python

# load libraries
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os
import yaml

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

# set plot title, axes labels, and ticks
ax.set_title(CONFIG['plot']['title'])
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

import matplotlib
matplotlib.use('Agg')
import os, sys, re, math,itertools
from pylab import *
from helper import *

rename = {
    "average": "   avg   "
}

lineconfig = {
# CC Algos
    'DL_DETECT'     : "ls='-', lw=2, color='#f15854', marker='o', ms=4",
    'NO_WAIT'       : "ls='-', lw=2, color='#faa43a', marker='D', ms=4",
    'WAIT_DIE'      : "ls='-', lw=2, color='#DECF3F', marker='s', ms=4",
    'TIMESTAMP'     : "ls='-', lw=2, color='#60BD68', marker='^', ms=4",
    'MVCC'          : "ls='--', lw=2, color='#5DA5DA', marker='o', ms=4", #, marker='+', ms=10",
    'OCC'           : "ls='--', lw=2, color='#B276B2', marker='+', ms=6",
    'HSTORE'        : "ls='-', lw=2, color='#4d4d4d', marker='x', ms=6",

# Multipartition Rates
    0               : "ls='-', lw=2, color='#f15854', marker='o', ms=4",
    1               : "ls='-', lw=2, color='#faa43a', marker='D', ms=4",
    10              : "ls='-', lw=2, color='#DECF3F', marker='s', ms=4",
    20              : "ls='-', lw=2, color='#60BD68', marker='^', ms=4",
    30              : "ls='--', lw=2, color='#5DA5DA', marker='o', ms=4", #, marker='+', ms=10",
    40              : "ls='--', lw=2, color='#B276B2', marker='+', ms=6",
    50              : "ls='-', lw=2, color='#4d4d4d', marker='s', ms=6",
    60              : "ls='-', lw=2, color='#f15854', marker='x', ms=6",
    70              : "ls='-', lw=2, color='#faa43a', marker='+', ms=6",
    80              : "ls='-', lw=2, color='#DECF3F', marker='o', ms=6",
    90              : "ls='-', lw=2, color='#60BD68', marker='D', ms=6",
    100             : "ls='-', lw=2, color='#5DA5DA', marker='s', ms=6",
}

# data[config] = []
# config : different configurations
# under a config, the list has the values for each benchmark 
# label : the names of benchmarks, matching the list

def draw_bar(filename, data, label, names=None, dots=None, 
        ylabel='Speedup', xlabel='', rotation=30,
        ncol=1, bbox=[0.95, 0.9], colors=None, hatches=None,
        figsize=(9, 3), left=0.1, bottom=0.18, right=0.96, top=None, 
        ylimit=None, xlimit=None):

    index = range(0, len(label))
    m_label = list(label)
    for i in range(0, len(label)):
        if m_label[i] in rename:
            m_label[i] = rename[ label[i] ]
    fig, ax1 = plt.subplots(figsize=figsize)
    ax1.set_ylabel(ylabel)
    ax1.set_xlabel(xlabel)
    ax1.axhline(0, color='black', lw=1)
    grid(axis='y')
    if dots != None:
        ax2 = ax1.twinx()
        ax2.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
        ax2.set_ylabel('Total Memory Accesses')
        ax2.set_ylim([0,12e6])
    width = 1.0 / len(data) / 1.6
    if colors == None :
        colors = [0] * len(data)
        for i in range(0, len(data)) :
            colors[i] = [0.1 + 0.7 / len(data) * i] * 3
    n = 0
    bars = [0] * len(data)
    if names == None: names = data.keys()
    if xlimit == None:
        xlimit = (-0.2,len(index) - 0.2)
    ax1.set_xlim(xlimit)
    if ylimit != None:
        ax1.set_ylim(ylimit)
    for cfg in names:
        ind = [x + width*n for x in index]
        hatch = None if hatches == None else hatches[n]
        bars[n] = ax1.bar(ind, data[cfg], width, color=colors[n], hatch=hatch)
        if dots != None:
            ax2.plot([x + width/2 for x in ind], dots[cfg], 'ro')
        n += 1
    plt.xticks([x + width*len(names)/2.0 for x in index], m_label, size='14', rotation=rotation)
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off', # ticks along the top edge are off
        labelbottom='on') # labels along the bottom edge are off

    fig.legend([x[0] for x in bars], names, prop={'size':12}, 
        ncol=ncol, bbox_to_anchor=bbox, labelspacing=0.2) 
    subplots_adjust(left=left, bottom=bottom, right=right, top=top)
    savefig('../figs/' + filename)


def draw_line(fname, data, xticks, 
        title = None,
        xlabels = None,
        bbox=(0.9,0.95), ncol=1, 
        ylab='Throughput', logscale=False, 
        logscalex = False,
        ylimit=0, xlimit=None, xlab='Number of Cores',
        legend=True, linenames = None, figsize=(23/3, 10/3), styles=None) :
    fig = figure(figsize=figsize)
    thr = [0] * len(xticks)
    lines = [0] * len(data)
    ax = plt.axes()
    if logscale :
        ax.set_yscale('log')
    if logscalex:
        ax.set_xscale('log')
    n = 0
    if xlabels != None :
        ax.set_xticklabels(xlabels) 
    if linenames == None :
        linenames = sorted(data.keys())
    for i in range(0, len(linenames)) :
        key = linenames[i]
        intlab = [float(x) for x in xticks]
        style = None
        if styles != None :
            style = styles[key]
        elif key in lineconfig.keys():
            style = lineconfig[key]
        else :
            style = lineconfig.values()[i]
        exec "lines[n], = plot(intlab, data[key], %s)" % style
        n += 1
    if ylimit != 0:
        ylim(ylimit)
    if xlimit != None:
        xlim(xlimit)
    plt.gca().set_ylim(bottom=0)
    ylabel(ylab)
    xlabel(xlab)
    if not logscale:
        ticklabel_format(axis='y', style='sci', scilimits=(-3,5))
#if logscalex:
#ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    if legend :
        fig.legend(lines, linenames, bbox_to_anchor = bbox, prop={'size':9}, ncol=ncol)
    subplots_adjust(left=0.18, bottom=0.15, right=0.9, top=None)
    if title:
        ax.set_title(title)

    axes = ax.get_axes()
    axes.yaxis.grid(True,
        linestyle='-',
        which='major',
        color='0.75'
    )
    ax.set_axisbelow(True)

    savefig('../figs/' + fname +'.pdf', bbox_inches='tight')

def draw_bars(data, xlabels, 
        figname='stack', 
        figsize=(8, 3),
        ylab = 'Throughput',
        xlab = 'Time',
        title = None,
        bbox=[0.95,0.95]):

    fig = figure(figsize=figsize)
    ind = range(0, len(xlabels))

    plots = ()

    #xlabels = [str(x) for x in xlabels]

    xticks( ind,  xlabels, rotation=30, ha='center')
    clr = itertools.cycle(['#DECF3F','#5DA5DA','#60BD68','#FAA43A','#DECF3F','#F15854','#4d4d4d'])
    htch = itertools.cycle(['','//','\\','-','\\\\','/'])

    w = 0.12
    k = 0
    for s in sorted(data.keys()):
        p = plt.bar([i+(w*k) for i in ind], data[s], color=clr.next(), hatch=htch.next(),width=w)
        plots = plots + (p,)
        k = k+1

    ax = plt.axes()
    ylabel(ylab)
    xlabel(xlab)
    if title:
        ax.set_title(title)
    legend(plots, sorted(data.keys()), bbox_to_anchor = bbox, prop={'size':11})
    subplots_adjust(bottom=0.25, right=0.7, top=None)
    savefig('../figs/' + figname + '.pdf', bbox_inches='tight')



def draw_stack(data, xlabels, slabels, figname='stack', figsize=(8, 3),ymin=0, ymax=1) :
    fig = figure(figsize=figsize)
    ind = range(0, len(xlabels))

    plots = ()
    bottom = [0] * len(xlabels)

    ylim([ymin, ymax])
    #xlabels = [str(x) for x in xlabels]

    xticks( ind,  xlabels, rotation=30, ha='center')
    clr = itertools.cycle(['#DECF3F','#5DA5DA','#60BD68','#FAA43A','#DECF3F','#F15854','#4d4d4d'])
    htch = itertools.cycle(['','//','\\','-','\\\\','/'])

    for s in range(len(slabels)):
        p = plt.bar(ind, data[s], color=clr.next(), hatch=htch.next(), bottom=bottom)
        plots = plots + (p,)
        bottom = [a + b for a,b in zip(bottom, data[s])]

    legend(reversed(plots), tuple(slabels), bbox_to_anchor = (0.38, -0.2, 1, 1), prop={'size':11})
    subplots_adjust(bottom=0.25, right=0.7, top=None)
    savefig('../figs/' + figname + '.pdf', bbox_inches='tight')


def draw_2line(x, y1, y2, figname="noname", ylimit=None):
#   fig = figure(figsize=(16/3, 9/3))
    fig, ax1 = plt.subplots(figsize=(21/3, 7.0/3))
    if ylimit != None:
        ax1.set_ylim(ylimit)
    #ax1.set_xscale('log')
    # ax1.plot(x, y1, 'b-', lw=2, marker='o', ms=4)
    color = (0.2,0.2,0.5)
    ax1.plot(range(0, len(x)), y1, ls='-', lw=2, color=color, marker='o', ms=4)
    ax1.set_xlabel('Timeout Threshold')
    ax1.set_xticklabels([str(i) for i in x])
    ax1.set_ylabel('Throughput (Million txn/s)', color=color)
    for tl in ax1.get_yticklabels():
        tl.set_color(color)

    ax2 = ax1.twinx()
    #ax2.set_ylim(bottom=0)
    # ax2.plot(x, y2, 'r-', lw=2, marker='s', ms=4)
    # ax2.plot(range(0, len(x)), y2, 'r--', lw=2, marker='s', ms=4)
    color = (1, 0.5, 0.5)
    ax2.plot(range(0, len(x)), y2, ls='--', lw=2, color=color, marker='s', ms=4)
    ax2.set_ylabel('Abort Rate', color=color)
    for tl in ax2.get_yticklabels():
        tl.set_color(color)
    #ax2.set_xticklabels([str(i) for i in x])
    ax2.set_xticklabels([str(i) for i in x])
    ax2.yaxis.grid(True,
                   linestyle='-',
                   which='major',
                   color='0.75'
    )
    subplots_adjust(left=0.18, bottom=0.15, right=0.9, top=None)

    savefig('../figs/' + figname + '.pdf', bbox_inches='tight')

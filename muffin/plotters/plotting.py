import matplotlib 
from matplotlib import pyplot as plt
import numpy 
import matplotlib.font_manager as fm# Collect all the font names available to matplotlib
import os
#fm = matplotlib.font_manager.json_load(os.path.expanduser("~/.cache/matplotlib/fontlist-v310.json"))
#fm.findfont("serif", rebuild_if_missing=False)

#matplotlib.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
#matplotlib.rc('text', usetex=True)

plt.rcParams['text.latex.preamble'] = r"\usepackage{bm}"

def set_font_to_latex():
    """
    Set font of ax labels to latex font. 
    Set use latex to true to use latex language.
    """
    #matplotlib.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    #matplotlib.rc('text', usetex=True)
    plt.rcParams['font.family'] = 'serif' 
    plt.rcParams['font.serif']  = 'Computer Modern'
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r"\usepackage{amsfonts}"

def set_bb_to_vec():
    """
    Use bm to embolden maths.

    """
    # previously used plt.rc('text.latex', preamble=r'\usepackage{bm}')
    # order matters, one is cancelling bm out
    plt.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"
    plt.rcParams['text.latex.preamble'] = r"\usepackage{amsbsy}"
    plt.rcParams['text.latex.preamble'] = r"\usepackage{amsfonts}"
    #plt.rcParams['text.latex.preamble'] = r'\usepackage{bm}'	
    


def set_font_size_for_ax_labels(fig_type="half_page"):
    """
    Set the global font_size.
    """
    if fig_type=="half_page":
        ax_label_font_size=24
    elif fig_type=="full_page":
        ax_label_font_size=18
    else: 
        raise Exception

    plt.rcParams['font.size'] = ax_label_font_size



def set_linewidth(linewidth=2.0):
    """
    Set global linewidth.
    """
    plt.rcParams['lines.linewidth'] = linewidth


def thesisify_pre_ax_creation(fig_type="half_page",linewidth=2.0):
    """
    """
    set_font_to_latex()

    set_bb_to_vec()

    set_font_size_for_ax_labels(fig_type=fig_type)
    
    set_linewidth(linewidth=linewidth)








#def thesisify_ax_creation(fig_type="half_page"):
#    """
#    Make figure and axis that has right dimensiosn for either full width of half width 
#    of page of thesis.
#    """
#    if fig_type == "full_page":
#        fig_size=[6.4, 4.8]
#    elif fig_type == "half_page":
#        fig_size=[3.2, 2.4]
#    fig, ax = plt.subplots(1,1, figsize=fig_size)
#    return fig, ax 







def set_ticks(ax, font_size=13, major_tick_length=5.0, minor_tick_length=2.5, major_tick_width=1.0, minor_tick_width=1.0):
    """
    Setup major and minor ticks
    https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.tick_params.html
    """
    ax.minorticks_on()

    # thesis
    #ax.xaxis.set_tick_params(which='major', length=major_tick_length, width=major_tick_width, direction='in', top=True  , labelsize=font_size, pad=6)
    #ax.xaxis.set_tick_params(which='minor', length=minor_tick_length, width=minor_tick_width, direction='in', top=True  , labelsize=font_size, pad=6)
    #ax.yaxis.set_tick_params(which='major', length=major_tick_length, width=major_tick_width, direction='in', right=True, labelsize=font_size, pad=6)
    #ax.yaxis.set_tick_params(which='minor', length=minor_tick_length, width=minor_tick_width, direction='in', right=True, labelsize=font_size, pad=6)

    # paper 
    ax.xaxis.set_tick_params(which='major', length=major_tick_length, width=major_tick_width, direction='in', top=False  , labelsize=font_size, pad=6)
    ax.xaxis.set_tick_params(which='minor', length=minor_tick_length, width=minor_tick_width, direction='in', top=False  , labelsize=font_size, pad=6)
    ax.yaxis.set_tick_params(which='major', length=major_tick_length, width=major_tick_width, direction='in', right=False, labelsize=font_size, pad=6)
    ax.yaxis.set_tick_params(which='minor', length=minor_tick_length, width=minor_tick_width, direction='in', right=False, labelsize=font_size, pad=6)

    return ax



def set_ax_labels(ax, x_label=None, y_label=None, labelpad=5):
    """
    """
    if x_label != None:
        ax.set_xlabel(x_label, labelpad=labelpad)
    if y_label != None:
        ax.set_ylabel(y_label, labelpad=labelpad)
    return ax



def set_ax_lims(ax,x_left=None,x_right=None,y_bottom=None,y_top=None):
    """
    Works best if these are max and min of x and y.
    """
    ax.set_xlim(left=x_left, right=x_right)
    ax.set_ylim(bottom=y_bottom, top=y_top)
    return ax


def set_legend(ax, font_size=13):
    """
    """
    ax.legend(loc="best", frameon=False, fontsize=font_size)
    return ax


def set_spines(ax, spines_on=False):
    """
    """
    if spines_on==False:
        # Hide the right and top spines # paper
        # ax.spines[['right', 'top']].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        pass # thesis
    return ax


def thesisify_post_plot(ax,
		         fig_type="half_page",
                 x_label=None,
                 y_label=None,
                 x_left=None,
                 x_right=None,
                 y_bottom=None,
                 y_top=None,
                 major_tick_length=5.0,
                 minor_tick_length=2.5,
                 major_tick_width=1.0,
                 minor_tick_width=1.0,
                 labelpad=5, 
		 spines_on=False):
    """
    """
    if fig_type=="half_page":
        ax_label_font_size=24
        ticks_font_size=18
        legend_font_size=18
    elif fig_type=="full_page":
        ax_label_font_size=18
        ticks_font_size=13.5
        legend_font_size=13.5
  
    #set_font_to_latex()
    
    #set_font_size_for_ax_labels(font_size=font_size)
    ax = set_ticks(ax=ax,
                   font_size=ticks_font_size, 
                   major_tick_length=major_tick_length, 
                   minor_tick_length=minor_tick_length, 
                   major_tick_width=major_tick_width,
                   minor_tick_width=minor_tick_width)
    
    ax = set_ax_lims(ax=ax,
                     x_left=x_left,
                     x_right=x_right,
                     y_bottom=y_bottom,
                     y_top=y_top)
    
    ax = set_ax_labels(ax=ax, 
                       x_label=x_label,
                       y_label=y_label,
                       labelpad=labelpad)

    ax = set_legend(ax=ax, font_size=legend_font_size)

    
    ax = set_spines(ax=ax,spines_on=spines_on)
    
    return ax







def save_fig(fig,fname,format="svg"):
    
    fig.tight_layout(pad=0.5)
    
    fig.savefig(fname=fname, format=format)





if __name__=="__main__":

    print(plt.rcParams.keys())

    x = numpy.linspace(-10,10,11)
    y = numpy.linspace(-10,100,11)


    thesisify_pre_ax_creation()

    fig, ax = plt.subplots(1,1)
    ax.plot(x,y,label="words")

    # once weve added everything we want to to axis...

    ax = thesisify_post_plot(ax=ax,
                      x_label=r'Wavelength $\alpha$ (nm)',
                      y_label=r'Absorbance $\beta  $(O.D.)',
                      x_left=min(x),
                      x_right=max(x),
                      y_bottom=min(y),
                      y_top=max(y))

    fig.savefig(fname="figure_name.svg")


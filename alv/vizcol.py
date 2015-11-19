import matplotlib.pyplot as pl
from matplotlib.colors import ListedColormap

##
# Predefined colormaps
##
standard_color_list = pl.rcParams['axes.color_cycle']

# up to 10 cycles
cm_std = ListedColormap(standard_color_list, N=len(standard_color_list)*10)

cm1 = ListedColormap(['blue', 'green', 'red', 'lightgray',
                      'orange', 'purple', 'navy', 'brown'], N=8)

cm2 = ListedColormap(['lightgray', 'green', 'red', 'orange',
                      'blue', 'purple', 'brown', 'navy'], N=8)

cm3 = ListedColormap(['lightgray', 'green', 'red', 'orange',
                      'blue', 'purple', 'brown', 'navy'
                      'gray', 'darkgreen', 'darkred', 'darkorange',
                      'darkblue', 'darkviolet', 'coral', 'azure' ], N=16)



##
# Helper functions
##

def cyclic_col(clist):
    """Return function returning colors cyclically from a list given index."""
    return lambda i: clist[i%len(clist)]


# could actually return a color map!
def stdcolors(i):
    return cyclic_col()



## Color bar example
#import matplotlib as mpl
#norm = mpl.colors.BoundaryNorm(np.arange(1,9), cm1.N)
#mpl.colorbar.ColorbarBase(pl.gca(),cmap=cm1,
#                          norm=norm, boundaries=np.arange(1,9))
# pl.show()

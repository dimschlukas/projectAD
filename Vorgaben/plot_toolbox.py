import matplotlib

matplotlib.use("Qt5Agg")

def run_from_ipython():
    """
    Erfolgt der Aufruf der Funktion in einer iPython (Jupyter) Umgebung?
    """
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def move_figure(plt, new_x=0, new_y=0, width=0, height=0):
    """
    Hilfsfunktion für das Verschieben eines Plotfensters.
    Als Voraussetzung gilt der Aufruf von "matplotlib.use("Qt5Agg")" im Anschluss
    an die Modulimporte.
    """
    mngr = plt.get_current_fig_manager()
    geom = mngr.window.geometry()
    if (width == 0) and (height == 0):
        x, y, dx, dy = geom.getRect()
        mngr.window.setGeometry(new_x, new_y, dx, dy)
    else:
        mngr.window.setGeometry(new_x, new_y, width, height)


if __name__ == '__main__':
    pass

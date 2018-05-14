import collections
import textwrap


# Formatting that is Specific Based on Chart Type
def min_max_scatter_formatter(fig, ax, xmin=None, xmax=None, ymin=None,
                              ymax=None, **kwargs):
    # Sets default min and max unless otherwise given
    if xmin:
        if xmax:
            ax.set_xlim(xmin, xmax)
        else:
            ax.set_xlim(left=xmin)
    elif xmax:
        ax.set_xlim(right=xmax)
    if ymin:
        if ymax:
            ax.set_ylim(ymin, ymax)
        else:
            ax.set_ylim(bottom=ymin)
    elif ymax:
        ax.set_ylim(top=ymax)

    return fig


def min_max_line_area_formatter(fig, ax, data, xmin=None, xmax=None, ymin=None,
                                ymax=None, **kwargs):
    # Sets default xlim and ylim for scatter and line charts
    if xmin:
        if xmax:
            ax.set_xlim(xmin, xmax)
        else:
            ax.set_xlim(xmin, None)
    elif xmax:
            ax.set_xlim(data.index.values.min(), xmax)
    if ymin:
        if ymax:
            ax.set_ylim(ymin, ymax)
        else:
            ax.set_ylim(ymin, None)
    elif ymax:
        ax.set_ylim(0, ymax)
    if not xmin and not xmax:
        ax.set_xlim(data.index.values.min(), data.index.values.max())
    if not ymin and not ymax:
        ax.set_ylim(0, None)

    return fig


def set_ticks_nonbar(fig, ax, xtick_loc=None, xticklabels=None,
                     ytick_loc=None, yticklabels=None, xyear=None,
                     yyear=None, **kwargs):
    """
    For xtick_loc the user can input any list of positive or negative
    digits. Values that are not an int or float raise an error. xtick_loc
    values need to be in the xmin-xmax range. xticklabels accepts any list
    of any amount of objects. If too many labels are given, an error does
    not raise. A user can chose the location of numeric tick labels by
    including '' in the list to take the place of empty tick label locations.
    """
    if xtick_loc:
        try:
            ax.set_xticks(xtick_loc)
        except AttributeError:
            print('You have provided invalid '
                  'xtick location.')
        if xticklabels:
            ax.set_xticklabels(xticklabels)
    if ytick_loc:
        if not isinstance(ytick_loc, collections.abc.Sequence):
            ytick_loc = [ytick_loc]
        try:
            ax.set_yticks(ytick_loc)
        except AttributeError:
            print('You have provided invalid '
                  'ytick location.')
        if yticklabels:
            ax.set_yticklabels(yticklabels)

    # Formats matplotlibs default setting of labels, sets labels
    if not xticklabels:
        xticklabels = ax.get_xticks()
        if len(ax.get_xticklabels()[0].get_text()) == 0:
            if max(xticklabels) >= 1000000:
                # Check to see if any labels need to be formatted as floats
                if any([i % 1000 for i in xticklabels]):
                    xticklabels = ['' if not i else f"{i / 1000:,}" for i in
                                   xticklabels]
                else:
                    xticklabels = ['' if not i else f"{i / 1000:,.0f}" for i in
                                   xticklabels]
                # Append a 'K' to labels to show that they have been truncated
                xticklabels = [i + 'K' if i else '' for i in xticklabels]
            else:
                if not xyear:
                    xticklabels = ['{:,.0f}'.format(i) for i in
                                   ax.get_xticks()]
                else:
                    xticklabels = [int(i) for i in ax.get_xticks()]
            ax.set_xticklabels(xticklabels)
    if not yticklabels:
        yticklabels = ax.get_yticks()
        if len(ax.get_yticklabels()[0].get_text()) == 0:
            if max(yticklabels) >= 1000000:
                if any([i % 1000 for i in yticklabels]):
                    yticklabels = ['' if not i else f"{i / 1000:,}" for i in
                                   yticklabels]
                else:
                    yticklabels = ['' if not i else f"{i / 1000:,.0f}" for i in
                                   yticklabels]
                yticklabels = [i + 'K' if i else '' for i in yticklabels]
            else:
                if not yyear:
                    yticklabels = ['{:,.0f}'.format(i) for i in
                                   ax.get_yticks()]
                else:
                    yticklabels = [int(i) for i in ax.get_yticks()]
            ax.set_yticklabels(yticklabels)

    return fig


def axis_labels_vbar(fig, ax, data, xyear=None, yyear=None, xticklabels=None,
                     ytick_loc=None, yticklabels=None, **kwargs):
    """
    xtick_loc not used in vertical_bar since the location will always
    be on the bar.
    """

    # Alerts user if the wrong number of labels was provided, sets labels
    if xticklabels:
        if len(xticklabels) < len(data.index):
            print('You have supplied too few x-axis labels. Please provide'
                  ' the correct number of labels. Input " " to '
                  'the list add a blank label.')
        elif len(xticklabels) > len(data.index):
            print('You have supplied too many x-axis labels.'
                  ' Please provide the correct number of labels.')
        ax.set_xticklabels(xticklabels)

    # Sets y-tick locations and labels if given
    if ytick_loc:
        if not isinstance(ytick_loc, collections.abc.Sequence):
            ytick_loc = [ytick_loc]
        try:
            ax.set_yticks(ytick_loc)
        except AttributeError:
            print('You have provided an invalid '
                  'ytick location.')
    if yticklabels:
        ax.set_yticklabels(yticklabels)

    # Formats matplotlibs default setting of labels, sets labels
    if not xticklabels:
        xticklabels = data.index.values
        if type(xticklabels[0]) != str:
            if max(xticklabels) >= 1000000:
                # Check to see if any labels need to be formatted as floats
                if any([i % 1000 for i in xticklabels]):
                    xticklabels = ['' if not i else f"{i / 1000:,}" for i in
                                   xticklabels]
                else:
                    xticklabels = ['' if not i else f"{i / 1000:,.0f}" for i in
                                   xticklabels]
                # Append a 'K' to labels to show that they have been truncated
                xticklabels = [i + 'K' if i else '' for i in xticklabels]
            else:
                if not xyear:
                    xticklabels = ['{:,.0f}'.format(i) for i in
                                   data.index.values]
                else:
                    xticklabels = [int(i) for i in data.index.values]
        ax.set_xticklabels(xticklabels)
    if not yticklabels:
        yticklabels = ax.get_yticks()
        if len(ax.get_yticklabels()[0].get_text()) == 0:
            if max(yticklabels) >= 1000000:
                if any([i % 1000 for i in yticklabels]):
                    yticklabels = ['' if not i else f"{i / 1000:,}" for i in
                                   yticklabels]
                else:
                    yticklabels = ['' if not i else f"{i / 1000:,.0f}" for i in
                                   yticklabels]
                yticklabels = [i + 'K' if i else '' for i in yticklabels]
            else:
                yticklabels = ['{:,.0f}'.format(i) for i in ax.get_yticks()]
        ax.set_yticklabels(yticklabels)

    # Informs the user to consider h-bar if labels are too long
    label = ax.xaxis.get_ticklabels()[0]
    if len(label.get_text()) == 4 and label.get_text().isdigit:
        if len(ax.xaxis.get_ticklabels()) > 12:
            for label in ax.xaxis.get_ticklabels()[1::2]:
                label.set_visible(False)
    else:
        length_list = []
        for item in ax.xaxis.get_ticklabels():
            length_list.append(len(item.get_text()))
            total_length = sum(length_list)
            if (len(item.get_text()) > 9) | \
                    (total_length > 49) | \
                    (len(item.get_text()) > 6 and
                     len(ax.xaxis.get_ticklabels()) > 7):
                print("You may want to consider using a horizontal_bar chart"
                      " so that all of your x-axis labels are readable. Use"
                      " the command --kind horizontal_bar")
                break

    return fig


def axis_labels_hbar(fig, ax, data, xtick_loc=None, xticklabels=None,
                     ytick_loc=None, yticklabels=None, yyear=None, **kwargs):
    if yticklabels:
        if len(yticklabels) < len(data.index):
            print('You have supplied too few y-axis labels. Please provide'
                  ' the correct number of labels. Input " " to '
                  'the list add a blank label.')
        elif len(yticklabels) > len(data.index):
            print('You have supplied too many y-axis labels.'
                  ' Please provide the correct number of labels.')
        ax.set_yticklabels(yticklabels)

    if xtick_loc:
        try:
            ax.set_xticks(xtick_loc)
        except AttributeError:
            print('You have provided an invalid '
                  'xtick location.')

    if xticklabels:
        ax.set_xticklabels(xticklabels)

    # Reduces size of labels greater than 6 digits
    if not xticklabels:
        xtick_labels = ax.get_xticks()
        if len(ax.get_xticklabels()[0].get_text()) == 0:
            if max(xtick_labels) >= 1000000:
                if any([i % 1000 for i in xtick_labels]):
                    xtick_labels = ['' if not i else f"{i / 1000:,}" for i in
                                    xtick_labels]
                else:
                    xtick_labels = ['' if not i else f"{i / 1000:,.0f}" for
                                    i in xtick_labels]
                xtick_labels = [i + 'K' if i else '' for i in xtick_labels]
            else:
                xtick_labels = ['{:,.0f}'.format(i) for i in ax.get_xticks()]
        ax.set_xticklabels(xtick_labels)
    if not yticklabels:
        yticklabels = data.index.values
        if type(yticklabels[0]) == int or type(yticklabels[0]) == float:
            if max(yticklabels) >= 1000000:
                if any([i % 1000 for i in yticklabels]):
                    yticklabels = ['' if not i else f"{i / 1000:,}" for i in
                                   yticklabels]
                else:
                    yticklabels = ['' if not i else f"{i / 1000:,.0f}" for i in
                                   yticklabels]
                yticklabels = [i + 'K' if i else '' for i in yticklabels]
            else:
                if not yyear:
                    yticklabels = ['{:,.0f}'.format(i) for i in
                                   yticklabels]
                else:
                    yticklabels = [int(i) for i in data.index.values]
        yticklabels = [textwrap.fill(i, 30) for i in yticklabels]
        ax.set_yticklabels(yticklabels)

    return fig

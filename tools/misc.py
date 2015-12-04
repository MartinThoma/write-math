#!/usr/bin/env python

"""
Miscallenious functions / classes which are needed by multiple tools
for write-math.com
"""

# My modules
from hwrt.handwritten_data import HandwrittenData


class HandwrittenDataM(HandwrittenData):
    """A modified version of HandwrittenData which has some GUI elements."""
    def __init__(self,
                 raw_data_json,
                 formula_id,
                 wild_point_count,
                 missing_line,
                 has_hook,
                 has_too_long_line,
                 is_image,
                 other_problem,
                 has_interrupted_line,
                 raw_data_id,
                 latex):
        HandwrittenData.__init__(self, raw_data_json, formula_id)
        self.wild_point_count = wild_point_count
        self.missing_line = missing_line
        self.has_hook = has_hook
        self.has_too_long_line = has_too_long_line
        self.is_image = is_image
        self.other_problem = other_problem
        self.has_interrupted_line = has_interrupted_line
        self.unaccept = False
        self.ok = False
        self.raw_data_id = raw_data_id
        self.latex = latex
        self.istrash = False

    def show(self):
        """Display a window with this recording."""
        import matplotlib.pyplot as plt
        from matplotlib.widgets import CheckButtons
        from matplotlib.widgets import Button
        fig, ax = plt.subplots()
        ax.set_title('Raw data id: %i, LaTeX: %s' % (self.raw_data_id,
                                                     self.latex))
        plt.subplots_adjust(bottom=0.3)

        for line in self.get_pointlist():
            xs, ys = [], []
            for p in line:
                xs.append(p['x'])
                ys.append(p['y'])
            ax.plot(xs, ys, '-o')
        ax.axis((0, 1, 0, 1))
        plt.gca().invert_yaxis()
        ax.set_aspect('equal')

        def handle_checkboxes(label):
            if label == 'other_problem':
                self.other_problem = not self.other_problem
            elif label == 'missing_line':
                self.missing_line = not self.missing_line
            elif label == 'has_hook':
                self.has_hook = not self.has_hook
            elif label == 'has_too_long_line':
                self.has_too_long_line = not self.has_too_long_line
            elif label == 'is_image':
                self.is_image = not self.is_image
            elif label == 'has_interrupted_line':
                self.has_interrupted_line = not self.has_interrupted_line
            plt.draw()

        checkpos = plt.axes([0.01, 0.05, 0.45, 0.2])
        check = CheckButtons(checkpos,
                             ('other_problem',
                              'has_interrupted_line',
                              'missing_line',
                              'has_hook',
                              'has_too_long_line',
                              'is_image'),
                             (self.other_problem,
                              self.has_interrupted_line,
                              self.missing_line,
                              self.has_hook,
                              self.has_too_long_line,
                              self.is_image))
        check.on_clicked(handle_checkboxes)

        def ok_function(*args):
            self.ok = True
            plt.close()
        okpos = plt.axes([0.7, 0.05, 0.1, 0.075])
        ok_button = Button(okpos, 'OK')
        ok_button.on_clicked(ok_function)

        def unaccept_function(*args):
            """
            Unaccept the classification of a recording and close the window.
            """
            self.unaccept = True
            print("unaccept raw_data_id %i" % self.raw_data_id)
            plt.close()
        unacceptpos = plt.axes([0.81, 0.05, 0.1, 0.075])
        unaccept_button = Button(unacceptpos, 'unaccept')
        unaccept_button.on_clicked(unaccept_function)

        def set_trash(a):
            """Set its argument to trash and close the window."""
            a.istrash = True
            print("trash raw_data_id %i" % self.raw_data_id)
            plt.close()
        is_trash_pos = plt.axes([0.7, 0.2, 0.1, 0.075])
        is_trash_button = Button(is_trash_pos, 'is_trash')
        is_trash_button.on_clicked(set_trash)

        # maximise height
        mng = plt.get_current_fig_manager()
        width, height = mng.window.maxsize()
        mng.resize(500, height)
        plt.axis('equal')
        plt.show()

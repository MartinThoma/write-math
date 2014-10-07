    def __call__(self, handwritten_data):
        assert isinstance(handwritten_data, HandwrittenData.HandwrittenData), \
            "handwritten data is not of type HandwrittenData, but of %r" % \
            type(handwritten_data)

        pointlist = handwritten_data.get_pointlist()

        # Calculate bounding box
        min_x, min_y = pointlist[0][0]['x'], pointlist[0][0]['y']
        max_x, max_y = pointlist[0][0]['x'], pointlist[0][0]['y']
        min_t = pointlist[0][0]['time']
        for stroke in pointlist:
            for point in stroke:
                min_x = min(min_x, point['x'])
                max_x = max(max_x, point['x'])
                min_y = min(min_y, point['y'])
                max_y = max(max_y, point['y'])
                min_t = min(min_t, point['time'])

        # Calculate paramters for scaling and shifting to
        # [−0.5, 0.5] × [−0.5, 0.5]
        width, height = max_x - min_x + 1, max_y - min_y + 1
        factor_x, factor_y = 1.0/width, 1.0/height
        factor = min(factor_x, factor_y)
        add_x, add_y = width*factor/2, height*factor/2

        # Move every single point of a recording
        pointlist = handwritten_data.get_pointlist()
        for strokenr, stroke in enumerate(pointlist):
            for key, p in enumerate(stroke):
                pointlist[strokenr][key] = {
                    "x": (p["x"] - min_x) * factor - add_x,
                    "y": (p["y"] - min_y) * factor - add_y,
                    "time": p["time"] - min_t}
                if "pen_down" in p:
                    pointlist[strokenr][key]["pen_down"] = p["pen_down"]

        # Save
        handwritten_data.set_pointlist(pointlist)

        assert self.max_width - handwritten_data.get_width() >= -0.00001, \
            "max_width: %0.5f; width: %0.5f" % (self.max_width,
                                                handwritten_data.get_width())
        assert self.max_height - handwritten_data.get_height() >= -0.00001, \
            "max_height: %0.5f; height: %0.5f" % \
            (self.max_height, handwritten_data.get_height())
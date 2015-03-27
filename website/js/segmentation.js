function mouseDownHandler(e) {
    startX = e.clientX;
    startY = e.clientY;
    redraw = true;
    lastClick = new Date().getTime();
}

/**
 * Find all paths which have at least one point in the rectangle
 * defined by x, y, width, height
 *
 * Return the ids of the paths
 */
function getContainedPaths() {
    var a = document.getElementById("canvas");
    var svgDoc = a.contentDocument;
    var paths = svgDoc.getElementsByTagName('path');

    var x_left = Math.min(startX, endX);
    var x_right = Math.max(startX, endX);
    var y_top = Math.min(startY, endY);
    var y_bottom = Math.max(startY, endY);

    var height = Math.abs(startY-endY)
    var width = Math.abs(startX-endX);

    var containedPaths = [];
    for (var i = 0; i < paths.length; i++) {
        var points = paths[i].pathSegList;
        for (var j = 0; j < points.length; j++) {
            var p = points[j];
            if (x_left < p.x && p.x < x_right && y_top < p.y && p.y < y_bottom) {
                containedPaths.push(parseInt(paths[i].id.replace(/^stroke/, '')));
                break;
            }
        };
    };
    return containedPaths;
}

function mouseUpEventHandler(e) {
    var uptime = new Date().getTime();
    if (uptime - lastClick < 90) {
        var a = document.getElementById("canvas");
        var svgDoc = a.contentDocument;
        var rect = svgDoc.getElementById('rectangleSelection');

        startX = 0;
        startY = 0;
        endX = 0;
        endY = 0;

        rect.setAttributeNS(null, 'x', 0);
        rect.setAttributeNS(null, 'y', 0);
        rect.setAttributeNS(null, 'height', 0);
        rect.setAttributeNS(null, 'width', 0);
    } else {
        endX = e.clientX;
        endY = e.clientY;
        var paths = getContainedPaths();
        if (paths.length > 0) {
            segmentation = re_segment(paths);
            colorBySegmentation()
            sendSegmentation(recording_id, segmentation);
        };
    };
    redraw = false;
}

function mouseMoveEventHandler(e) {
    if (redraw) {
        var a = document.getElementById("canvas");
        var svgDoc = a.contentDocument;
        var rect = svgDoc.getElementById('rectangleSelection');

        endX = e.clientX;
        endY = e.clientY;

        var x = Math.min(startX, endX);
        var y = Math.min(startY, endY);
        var height = Math.abs(startY-endY)
        var width = Math.abs(startX-endX);

        rect.setAttributeNS(null, 'x', x);
        rect.setAttributeNS(null, 'y', y);
        rect.setAttributeNS(null, 'height', height);
        rect.setAttributeNS(null, 'width', width);
    };
}

function contains(a, obj) {
    var i = a.length;
    while (i--) {
       if (a[i] === obj) {
           return true;
       }
    }
    return false;
}

function re_segment(selection) {
    var new_segmentation = [];
    for (var i = 0; i < segmentation.length; i++) {
        var new_symbol = [];
        var old_symbol = segmentation[i];
        for (var j = 0; j < old_symbol.length; j++) {
            var stroke_id = old_symbol[j];
            if (!contains(selection, stroke_id)) {
                new_symbol.push(stroke_id);
            };
        };
        if (new_symbol.length > 0) {
            new_symbol.sort();
            new_segmentation.push(new_symbol);
        };
    };
    new_segmentation.push(selection);
    new_segmentation.sort(function(a, b) {
        return a[0]-b[0];
    });
    segmentation = new_segmentation;
    return segmentation;
}


function colorBySegmentation() {
    var a = document.getElementById('canvas');
    var svgDoc = a.contentDocument;

    var colors = [
        "#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
        "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
        "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
        "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
        "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
        "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
        "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
        "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",

        "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
        "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
        "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
        "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
        "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
        "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
        "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
        "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58"];

    for (var symbol_i = 0; symbol_i < segmentation.length; symbol_i++) {
        symbol = segmentation[symbol_i];
        for (var stroke_i = 0; stroke_i < symbol.length; stroke_i++) {
            stroke_id = symbol[stroke_i];
            svgDoc.getElementById('stroke'+stroke_id).style.stroke = colors[symbol_i % colors.length];
        };
    };
}

function sendSegmentation(id, segmentation) {
    console.log(JSON.stringify(segmentation));
    $('#segmentation').val(JSON.stringify(segmentation));
    $.ajax({
      type: "POST",
      url: "../api/set-segmentation.php",
      data: {'recording_id': id, 'segmentation': JSON.stringify(segmentation)},
      success: function(data)
        {
            console.log(data);
        },
      dataType: "json",
      error: function(xhr, status, error) {
            console.log("Error while sending the segmentation:");
            console.log(status);
            console.log(error);
      }
    });
}
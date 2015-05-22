// Visualize which strokes were classified

function visualizeSymbolStrokes(tag) {
    var strokes = tag.getAttribute('data-strokes').split(',').map(function(item) {
        return parseInt(item, 10);
    });;
    var svgDoc = tag.contentDocument;
    console.log(strokes);
    for (var i = 100 - 1; i >= 0; i--) {
        var stroke = svgDoc.getElementById('stroke'+i);
        //console.log(stroke);
        if (stroke) {
            if (strokes.indexOf(i) > -1) {
                stroke.style.stroke = '#ff0000';
            } else {
                stroke.style.stroke = '#000000';
            }
            //stroke.style.fill = '#000000';
            //console.log("done");
        };
    };
    //svgDoc.getElementById('stroke'+stroke_id).style.stroke
}
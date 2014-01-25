canvasWidth = document.documentElement.getElementsByTagName('body')[0].clientWidth - 1;
canvasHeight = document.documentElement.clientHeight - 25;

context = document.getElementById('myCanvas').getContext("2d");
canvas = document.getElementById('myCanvas');
canvas.setAttribute('width', canvasWidth);
canvas.setAttribute('height', canvasHeight);

if(typeof G_vmlCanvasManager != 'undefined') {//IE
	canvas = G_vmlCanvasManager.initElement(canvas);
}
context = canvas.getContext("2d");

canvas.addEventListener('mousedown', mouseDownEventHandler);
canvas.addEventListener('touchstart', touchstartEventHandler);
function mouseDownEventHandler(e){
    console.log("mouseDownEventHandler");
  paint = true;
  if(paint){
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, false);
    redraw();
  }
}

function touchstartEventHandler(e){
    console.log("touchstartEventHandler");
  paint = true;
  if(paint){
    addClick(e.touches[0].pageX - this.offsetLeft, e.touches[0].pageY - this.offsetTop, false);
    redraw();
  }
}

canvas.addEventListener('mouseup', mouseUpEventHandler);
canvas.addEventListener('touchend', mouseUpEventHandler);
function mouseUpEventHandler(e){
    console.log("mouseUpEventHandler");
  paint = false;
}

/*canvas.addEventListener('mouseleave', mouseLeaveEventHandler);
function mouseLeaveEventHandler(e){
  paint = false;
}*/

canvas.addEventListener('mousemove',mouseMoveEventHandler);
canvas.addEventListener('touchmove',touchMoveEventHandler);
function mouseMoveEventHandler(e){
console.log("mouseMoveEventHandler");
  if(paint){
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
    redraw();
  }
}

function touchMoveEventHandler(e){
console.log("touchMoveEventHandler");
  if(paint){
    addClick(e.touches[0].pageX - this.offsetLeft, e.touches[0].pageY - this.offsetTop, true);
    redraw();
  }
}

var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

function addClick(x, y, dragging)
{
  clickX.push(x);
  clickY.push(y);
  clickDrag.push(dragging);
}

function redraw(){
  context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
  
  context.strokeStyle = "#df4b26";
  context.lineJoin = "round";
  context.lineWidth = 5;
			
  for(var i=0; i < clickX.length; i++) {		
    context.beginPath();
    if(clickDrag[i] && i){
      context.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       context.moveTo(clickX[i]-1, clickY[i]);
     }
     context.lineTo(clickX[i], clickY[i]);
     context.closePath();
     context.stroke();
  }
}

function clearDr() {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
    clickX = new Array();
    clickY = new Array();
    clickDrag = new Array();
}
/*
 function writeMessage(message) {
    text.setText(message);
    layer.draw();
  }
  
  var stage = new Kinetic.Stage({
    container: 'container',
    width: 800,
    height: 800
  });
  var layer = new Kinetic.Layer();

  var text = new Kinetic.Text({
    x: 10,
    y: 10,
    fontFamily: 'Calibri',
    fontSize: 24,
    text: '',
    fill: 'black'
  });
  
  var rectangle = new Kinetic.Rect({
    x: 0,
    y: 0,
    width: 800,
    height: 800,
    fill: '#cdcdcd',
    stroke: 'black',
    strokeWidth: 4
  });

  stage.on('touchmove', function() {
    var touchPos = stage.getPointerPosition();
    var x = touchPos.x - 190;
    var y = touchPos.y - 40;
    writeMessage('x: ' + x + ', y: ' + y);
  });

  stage.on('mousemove', function() {
    var touchPos = stage.getPointerPosition();
    var x = touchPos.x - 190;
    var y = touchPos.y - 40;
    writeMessage('x: ' + x + ', y: ' + y);
  });

  layer.add(rectangle);
  layer.add(text);
  stage.add(layer);
*/

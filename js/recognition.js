/*jslint browser:true */
"use strict";
var canvasWidth = document.documentElement.getElementsByTagName('body')[0].clientWidth - 1;
var canvasHeight = document.documentElement.clientHeight - 25;

var context = document.getElementById('sheet').getContext("2d");
var canvas = document.getElementById('sheet');
canvas.setAttribute('width', canvasWidth);
canvas.setAttribute('height', canvasHeight);
context = canvas.getContext("2d");

var clickX = [];
var clickY = [];
var clickDrag = [];
var paint;

/**
 * Add information where the user clicked at.
 * @param {number} x
 * @param {number} y
 * @return {boolean} dragging
 */
function addClick(x, y, dragging) {
    clickX.push(x);
    clickY.push(y);
    clickDrag.push(dragging);
}

function redraw() {
    // Clears the canvas
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);

    context.strokeStyle = "#ff0000";
    context.lineJoin = "round";
    context.lineWidth = 5;

    for (var i = 0; i < clickX.length; i++) {
        context.beginPath();
        if (clickDrag[i] && i) {
            context.moveTo(clickX[i - 1], clickY[i - 1]);
        } else {
            context.moveTo(clickX[i] - 1, clickY[i]);
        }
        context.lineTo(clickX[i], clickY[i]);
        context.closePath();
        context.stroke();
    }
}

function mouseDownEventHandler(e) {
    paint = true;
    var x = e.pageX - canvas.offsetLeft;
    var y = e.pageY - canvas.offsetTop;
    if (paint) {
        addClick(x, y, false);
        redraw();
    }
}

function touchstartEventHandler(e) {
    paint = true;
    if (paint) {
        addClick(e.touches[0].pageX - canvas.offsetLeft, e.touches[0].pageY - canvas.offsetTop, false);
        redraw();
    }
}

function mouseUpEventHandler(e) {
    context.closePath();
    paint = false;
}

function mouseMoveEventHandler(e) {
    var x = e.pageX - canvas.offsetLeft;
    var y = e.pageY - canvas.offsetTop;
    if (paint) {
        addClick(x, y, true);
        redraw();
    }
}

function touchMoveEventHandler(e) {
    if (paint) {
        addClick(e.touches[0].pageX - canvas.offsetLeft, e.touches[0].pageY - canvas.offsetTop, true);
        redraw();
    }
}

function clearDr() {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
    clickX = new Array();
    clickY = new Array();
    clickDrag = new Array();
}

function mouseWins(e) {
    setUpHandler(true, e);
}

function touchWins(e) {
    setUpHandler(false, e);
}

canvas.addEventListener('mousedown', mouseWins);
canvas.addEventListener('touchstart', touchWins);

function removeRaceHandlers() {
    canvas.removeEventListener('mousedown', mouseWins);
    canvas.removeEventListener('touchstart', touchWins);
}

function setUpHandler(isMouseandNotTouch, detectEvent) {
    removeRaceHandlers();
    if (isMouseandNotTouch) {
        canvas.addEventListener('mouseup', mouseUpEventHandler);
        canvas.addEventListener('mousemove', mouseMoveEventHandler);
        canvas.addEventListener('mousedown', mouseDownEventHandler);
        mouseDownEventHandler(detectEvent)
    } else {
        canvas.addEventListener('touchstart', touchstartEventHandler);
        canvas.addEventListener('touchmove', touchMoveEventHandler);
        canvas.addEventListener('touchend', mouseUpEventHandler);
        touchstartEventHandler(detectEvent)
    }
}
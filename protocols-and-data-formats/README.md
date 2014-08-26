## PowerPoint User Story

A user wants to do a PowerPoint presentation. That presentation contains some
math. So he clicks on "Insert > Formula... ". Now a Browser windows opens:

1. He has to login into 'Write Math'
2. If he has a device registered at 'Write Math', he gets a suggestion:
   "You can continue drawing the formula on this device, but you can also use the following devices:"
3. If 

## Device calibration

TODO

## Sending data to the server

When you want to send data of handwritten lines to the server, you have to 
access `write-math.com/receive.php?data=[Your data]`. `Your data` has to be
`JSON` encoded. It is a list of lines. Every line is a list of int-tuples:

```javascript
{"t" : t, "x": x, "y": y}
```

where `t` is in milliseconds, starting with 0 and strictly increasing with
every dot / every line.

`(x, y)` is the coordinate of the point where `(0, 0)` is the left upper corner.
No resizing should be done.

All three values, `t`, `x` and `y` should be integers and in `[0, 268435455]`.

TODO: Audio data?

## Receiving data from the server

`write-math.com/recognition.php?sessionId=[Your session id]`
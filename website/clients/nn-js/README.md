Although numericjs seems to allow (fast, tested?) matrix multiplication,
the problem of client-side neural net evaluation is that the parameters
have to be at the client side.

* Every parameter is a float. A float requires 4 byte.
* A 160:500:369 topology requires a 160×500 and a 500×369 matrix for the weights
  and a 500 vector and another 369 vector for the bias.
  That is `160*500 + 500*369 + 500 + 369 = 265369` floats.
* 265369 floats * 4 byte / float = 1061476 byte ≈ 8.5 MB

8.5 MB is too much for simply letting the client load it.
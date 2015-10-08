[![Build Status](https://travis-ci.org/MartinThoma/write-math.svg?branch=master)](https://travis-ci.org/MartinThoma/write-math)
[![Coverage Status](https://coveralls.io/repos/MartinThoma/write-math/badge.png)](https://coveralls.io/r/MartinThoma/write-math)
[![Code Issues](http://www.quantifiedcode.com/api/v1/project/dee640dc587341a9ad8a05e6ae4471e1/badge.svg)](http://www.quantifiedcode.com/app/project/dee640dc587341a9ad8a05e6ae4471e1)

write-math
==========

On-line recognition of mathematical formulae.

## Technology
Client-Side:
* HTML
* CSS
* JavaScript
  * fabric.js (see [example](http://fabricjs.com/freedrawing/), [tutorial](http://fabricjs.com/fabric-intro-part-4/))
  * [mathjax](http://www.mathjax.org/) for rendering LaTeX

Server-Side:
* Currently PHP+Python, but I'm thinking about switching (Haskell, Scala, Python, PHP, Java, C, C++?)


## TODO

http://scikit-learn.org/stable/modules/hmm.html

webdemo.myscript.com - seems to be pretty good!


how can I get equidistant points on a curve
* http://www.mathworks.com/matlabcentral/newsreader/view_thread/317568
* http://www.mathworks.com/matlabcentral/fileexchange/34874-interparc

## Important Misc

* [IAPR-TC11:Reading Systems](http://www.iapr-tc11.org/mediawiki/index.php/IAPR-TC11:Reading_Systems)
  * [Datasets](http://www.iapr-tc11.org/mediawiki/index.php/Datasets)
* Journals:
  * International Journal on Document Analysis and Recognition (IJDAR)
* Conferences:
  * ICDAR (International Conference on Document Analysis and Recognition)
  * IWFHR (International Workshop on Frontiers in Handwriting Recognition)
* http://www.isical.ac.in/~crohme/



* http://saskatoon.cs.rit.edu/inkml_viewer/
* http://www.isical.ac.in/~crohme/CROHME_data.html
* http://www.isical.ac.in/~crohme/data2.html


## Regular Cleanup / updates

To make sure that the user experience is good, execute the following scripts
on a regular basis:

* `tools/create_testset_online_once.py`: It adds new recordings to the test set
  - make sure that they are correct!
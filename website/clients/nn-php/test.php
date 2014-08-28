<?php

/**
 * Debugging
 */


function display_matrix($A) {
    $str = "<br/>";
    for ($i=0; $i < count($A); $i++) { 
        for ($j=0; $j < count($A[0]); $j++) { 
            $str .= $A[$i][$j]." ";
        }
        $str .= "<br/>";
    }
    echo $str;
}

function get_shape($matrix) {
    return array(count($matrix), count($matrix[0]));
}

/**
 * Model
 */

function apply_model($model, $x, $ranges, $means) {
    $i = 0;

    # Preprocessing
    # TODO

    if (count($means) != count($x[0])) {
        echo "Error! Dimension of means and of x is not equal!";
        echo "means dimension was ".count($means).", but x was ".count($x);
    }

    for ($i=0; $i < count($x[0]); $i++) { 
        $x[0][$i] = ($x[0][$i] - $means[$i]) / $ranges[$i];
    }

    foreach ($model as $layer) {
        $i+=1;
        $W = $layer['W'];
        $b = $layer['b'];
        $x = ikjMatrixProduct($x, $W);
        $x = apply_componentwise($x, 'sigmoid');
        $x = subtract($x, $b);
    }
    $x = softmax($x);
    /* flatten */
    $flat = array();
    for ($i=0; $i < count($x[0]); $i++) { 
        $flat[] = $x[0][$i];
    }
    return $flat;
}

/**
 * Multiply two matrices
 * @param  matrix $A mxn-matrix
 * @param  matrix $B nxk-matrix
 * @return matrix    mxk-matrix
 */
function ikjMatrixProduct($A, $B) {
    $m = count($A);
    $n = count($B[0]);
    $o = count($B);

    # Build the base array
    $C = array();
    for ($i=0; $i < $m; $i++) {
        $row = array();
        for ($j=0; $j < $n; $j++) {
            $row[] = 0.0;
        }
        $C[] = $row;
    }

    # Calculate
    for($i=0; $i < $m; $i++){
        for($k=0; $k < $o; $k++) {
            for($j=0; $j < $n; $j++) {
                $a = $A[$i][$k];
                $b = $B[$k][$j];
                $C[$i][$j] += $a * $b;
            }
        }
    }
    return $C;
}

function apply_componentwise($x, $f) {
    for ($i=0; $i < count($x[0]); $i++) { 
        $x[0][$i] = $f($x[0][$i]);
    }

    return $x;
}

function sigmoid($x) {
    return 1.0 / (1.0 + exp(-$x));
}

function subtract($x, $b) {
    for ($i=0; $i < count($x[0]); $i++) { 
        $x[0][$i] -= $b[0][$i];
    }
    return $x;
}

function softmax($w) {
    $sum = 0.0;
    for ($i=0; $i < count($w[0]); $i++) { 
        $w[0][$i] = exp($w[0][$i]);
        $sum += $w[0][$i];
    }
    for ($i=0; $i < count($w[0]); $i++) { 
        $w[0][$i] /= $sum;
    }
    return $w;
}

$json = file_get_contents("modelparams.json");
$model = json_decode($json, true);

$featurenormalization = trim(file_get_contents("featurenormalization.csv"));
$splitted = split("\n", $featurenormalization);
$means = array();
$ranges = array();
for ($i=0; $i < count($splitted); $i++) { 
    $tmp = split(";", $splitted[$i]);
    $means[] = floatval($tmp[0]);
    $ranges[] = floatval($tmp[1]);
}

$x = array(array());
for ($i=0; $i < 161; $i++) { 
    $x[0][] = 0.0;
}
$x = apply_model($model, $x, $ranges, $means);
var_dump($x);

?>
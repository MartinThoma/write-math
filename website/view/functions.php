<?php

require_once('../latex.php');

function remove_usepackage($package) {
    if (0 === strpos($package, '\usepackage{') && substr($package, -1) == '}') {
        $package = substr($package, strlen('\usepackage{'));
        $package = rtrim($package, '}');
    }
    return $package;
}

function sanitize_packages($packages) {
    if (strpos($packages, ';') !== false) {
        $packages = explode(';', $packages);
    } else {
        $packages = array($packages);
    }

    $packages = array_map(trim, $packages);
    $packages = array_map(remove_usepackage, $packages);

    return $packages;
}

function endsWith($haystack, $needle) {
    return $needle === "" || substr($haystack, -strlen($needle)) === $needle;
}

?>
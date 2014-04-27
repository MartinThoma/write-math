<?php

function get_path($data) {
    $path = "";
    $data = json_decode($data);
    foreach ($data as $line) {
      foreach ($line as $i => $point) {
        if ($i == 0) {
          $path .= " M ".$point->x." ".$point->y;
        } else {
          $path .= " L ".$point->x." ".$point->y;
        }
      }
    }
    return $path;
}

?>
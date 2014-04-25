<?php
require("config.php");
$link = mysql_connect ($server, $username, $password)
                      or die("Could not connect to database.");
mysql_select_db($dbname, $link) or die('Could not select database.');

/**
 * Parse JSON encoded data string that represents a set of handdrawn lines.
 * 
 * @param  string $data JSON encoded string that represents a set of handdrawn
 *         lines. It is of this format:
 *         [
 *           [
 *             {"t":   0, "x": 123, "y": 42},
 *             {"t": 123, "x": 125, "y": 43},
 *             {"t": 126, "x": 126, "y": 45}
 *           ],
 *           [ {"t": 128, "x": 127, "y": 44}]
 *         ]
 *         Test with this:
 *         [[{"t":   0, "x": 123, "y": 42}, {"t": 123, "x": 125, "y": 43}, {"t": 126, "x": 126, "y": 45}], [ {"t": 128, "x": 127, "y": 44}]]
 * @return Array of objects
 */
function parse_data($data){
    $data = json_decode ($data);

    // Test if data is valid
    $is_valid = true;
    $last_time = -1;
    foreach ($data as $line) {
        foreach ($line as $point) {
            if(array_key_exists("t", $point)) {
                if ($last_time < $point->t) {
                    $last_time = $point->t;
                } else {
                    echo "Time has to be strictly increasing";
                    $is_valid = false;
                    break 2;
                }
            } else {
                echo "A time value 't' has to exist.";
                $is_valid = false;
                break 2;
            }

            if(array_key_exists("x", $point) && array_key_exists("y", $point)) {
                if ($point->x < 0 || $point->y < 0) {
                    echo "Both, 'x' and 'y' have to be non-negative.";
                    $is_valid = false;
                    break 2;
                }

                if ($point->x >= 268435456 || $point->y >= 268435456) {
                    echo "Both, 'x' and 'y' have to be strictly smaller than 268435456.";
                    $is_valid = false;
                    break 2;
                }
            } else {
                echo "A 'x' and a 'y' value have to exist.";
                $is_valid = false;
                break 2;
            }
        }
    }
    return $data;
}

/**
 * Get an ID for the current session.
 * @return int Session ID
 */
function get_session_id() {
    //TODO
    return 0;
}

/**
 * Insert data into the database.
 * @param  list   $data        representation of handdrawn image in JSON format
 * @param  int    $session_id 
 * @param  int    $user_id
 * @return [type]             [description]
 */
function insert_data($data, $user_id, $session_id=0) {
    if($session_id==0) {
        //TODO: Prefix-check
        //TODO: insert
    } else {
        //TODO: update
    }
}

if(isset($_GET['data'])) {
    $session_id = get_session_id();

    $data = parse_data($_GET['data']);
    insert_data(json_encode($data), $session_id);
    echo "OK";
}
?>
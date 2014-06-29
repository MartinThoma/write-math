<?php

if (!function_exists('json_last_error_msg')) {
    function json_last_error_msg() {
        static $errors = array(
            JSON_ERROR_NONE             => null,
            JSON_ERROR_DEPTH            => 'Maximum stack depth exceeded',
            JSON_ERROR_STATE_MISMATCH   => 'Underflow or the modes mismatch',
            JSON_ERROR_CTRL_CHAR        => 'Unexpected control character found',
            JSON_ERROR_SYNTAX           => 'Syntax error, malformed JSON',
            JSON_ERROR_UTF8             => 'Malformed UTF-8 characters, possibly incorrectly encoded'
        );
        $error = json_last_error();
        return array_key_exists($error, $errors) ? $errors[$error] : "Unknown error ({$error})";
    }
}

function insert_userdrawing($user_id, $data) {
    global $pdo, $msg;

    $linelist = json_decode($data);
    $pointlist = array();
    foreach ($linelist as $line) {
        foreach ($line as $p) {
            $pointlist[] = array("x"=>$p->x, "y"=>$p->y);
        }
    }

    if (count($pointlist) == 0) {
        $msg[] = array("class" => "alert-danger",
                       "text" => "This could not be inserted. It didn't even ".
                                 "have a single point (ERR 2). You sent:<br/>".
                                 "<pre>".$data."</pre>");
        return false;
    } else {
        if (strpos($data, "[]") === false) {
            // Search dataset in database to prevent the database from throwing an
            // error to the user if its already present (e.g. multiple form submission)
            $sql = "SELECT `id` FROM `wm_raw_draw_data` ".
                   "WHERE `md5data` = MD5(:data);";
            $stmt = $pdo->prepare($sql);
            $stmt->bindParam(':data', $data, PDO::PARAM_STR);
            $stmt->execute();
            $raw_data_set = $stmt->fetchObject();
            if ($raw_data_set === False) {
                $sql = "INSERT INTO `wm_raw_draw_data` (".
                       "`user_id`, ".
                       "`data`, ".
                       "`md5data`, ".
                       "`creation_date`, ".
                       "`user_agent`, ".
                       "`accepted_formula_id`".
                       ") VALUES (:user_id, :data, MD5(data), ".
                       "CURRENT_TIMESTAMP, :user_agent, NULL);";
                $stmt = $pdo->prepare($sql);
                $uid = get_uid();
                $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
                $stmt->bindParam(':data', $data, PDO::PARAM_STR);
                $stmt->bindParam(':user_agent',
                                 $_SERVER['HTTP_USER_AGENT'],
                                 PDO::PARAM_STR);
                $stmt->execute();
                $raw_data_id = $pdo->lastInsertId();

                create_raw_data_svg($raw_data_id, $data);

                return $raw_data_id;
            } else {
                $msg[] = array("class" => "alert-warning",
                               "text" => "You've already submitted this data. ".
                                         "Please wait 5 seconds. This time is ".
                                         "needed to compare your drawing with ".
                                         "4000 others.");
                return $raw_data_set->id;
            }
        } else {
        $msg[] = array("class" => "alert-danger",
                       "text" => "This could not be inserted. It didn't even ".
                                 "have a single point. You sent:<br/>".
                                 "<pre>".$data."</pre> ".
                                 "At the moment I have problems with single ".
                                 "points. This might be a symptom of those ".
                                 "problems. See <a href=\"https://github.com/MartinThoma/write-math/issues/6\">issue 6</a>.");
        return false;
        }
    }
}

function insert_worker_answers($worker_id, $raw_data_id, $answer_json) {
    global $pdo;
    // Delete all answers regarding this raw_data_id from the current
    // worker
    $sql = "DELETE FROM `wm_worker_answers` WHERE `worker_id` = :wid ".
           "AND `raw_data_id` = :raw_data_id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':wid', $worker_id, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    // Insert new data
    foreach ($answer_json as $key => $object) {
        $formula_id = array_keys($object)[0];
        $probability = $object[$formula_id];
        $sql = "INSERT INTO `wm_worker_answers` (".
                "`worker_id` , ".
                "`raw_data_id` , ".
                "`formula_id` , ".
                "`probability` ".
                ") VALUES (:wid, :raw_data_id, :formula_id, :probability)";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':wid', $worker_id, PDO::PARAM_INT);
        $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
        $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
        $stmt->bindParam(':probability', $probability, PDO::PARAM_STR);
        try {
          $stmt->execute();
        } catch (Exception $e) {
          var_dump($e);
        }
    }
}

function classify($raw_data_id, $drawnJSON) {
    global $msg, $pdo;

    # Get a list of all workers
    $sql = "SELECT `id`, `worker_name`, `url` ".
           "FROM `wm_workers` ".
           "WHERE `latest_heartbeat` IS NOT NULL AND status = 'active'";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $workers = $stmt->fetchAll();

    # TODO: Make this asynchronous
    # Send classification request to all workers
    foreach ($workers as $worker) {
        $request_url = $worker['url'];
        // contact worker
        //set POST variables
        $url = $request_url;
        $fields = array('classify' => urlencode($drawnJSON));

        //url-ify the data for the POST
        $fields_string = "";
        foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
        rtrim($fields_string, '&');

        //open connection, set the url, number of POST vars, POST data
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, count($fields));
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fields_string);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $answer = curl_exec($ch);
        curl_close($ch);
        // end contact worker

        $answer_json = json_decode($answer, true);

        if (!(json_last_error() == JSON_ERROR_NONE)) {
            $msg[] = array("class" => "alert-warning",
               "text" => "Worker '".$worker['worker_name']."' returned '".
                         json_last_error_msg()."'<br/>".
                         "Request URL: <a href=\"$request_url\">Link</a><br/>".
                         "Answer: ".htmlentities(substr($answer, 0, 20)).
                         "...");
             # TODO: The user should not see this. This should be logged, though.
        } else {
            insert_worker_answers($worker['id'], $raw_data_id, $answer_json);
        }
    }
    header("Location: ../view/?raw_data_id=".$raw_data_id);
}

?>
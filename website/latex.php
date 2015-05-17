<?php

function chunk_math($text){
    # Fail when '{' and '}' don't match - be aware of escaped symbols!
    $opened_braces = 0;
    $last_char = '';
    foreach (str_split($text) as $char) {
        if ($char == '{' && $last_char != '\\') {
            $opened_braces += 1;
        }
        if ($char == '}' && $last_char != '\\') {
            $opened_braces -= 1;
            if ($opened_braces < 0) {
                throw new Exception("Braces don't match: ".$text);
            }
        }
        $last_char = $char;
    }

    if ($opened_braces != 0) {
        throw new Exception("$opened_braces braces are still open");
    }

    # Parse
    $single_symbol = ['_', '^', '&', '{', '}'];
    $breaking_chars = array_merge(['\\', ' '], $single_symbol);

    $chunks = [];
    $current_chunk = '';
    $lettersdigits = array_merge(range('A', 'Z'), range('a', 'z'), range('0', '9'));

    foreach (str_split($text) as $char) {
        if ($current_chunk == ''){
            $current_chunk = $char;
            continue;
        }
        if ($char == '\\') {
                    if ($current_chunk == '\\') {
                        $current_chunk .= $char;
                        $chunks[] = $current_chunk;
                        $current_chunk = '';
                    } else {
                        $chunks[] = $current_chunk;
                        $current_chunk = $char;
                    }
        } else if ($current_chunk == '\\' && in_array($char, $breaking_chars)) { # escaped
            $current_chunk .= $char;
            $chunks[] = $current_chunk;
            $current_chunk = '';
        } else if (in_array($char, $breaking_chars)) {
            $chunks[] = $current_chunk;
            $current_chunk = $char;
        } else if (in_array($char, $lettersdigits) && $current_chunk[0] == '\\') {
            $current_chunk .= $char;
        } else {
            $chunks[] = $current_chunk;
            $current_chunk = $char;
        }
    }

    # Add the last chunk
    if ($current_chunk != '') {
        $chunks[] = $current_chunk;
    }
    $filtered = [];
    foreach ($chunks as $chunk) {
        $arr_values = array_values($filtered);
        if (count($filtered) > 0 && end($arr_values) == ' ' && $chunk == ' '){
            continue;
        }
        $filtered[] = $chunk;
    }

    return $filtered;
}

function chunks_to_string($chunks) {
    $string = '';
    $began_context = False;
    $context_depth = 0;
    $context_triggers = ['_', '^'];
    foreach ($chunks as $chunk) {
        if ($began_context && $chunk != '{') {
            $string .= '{'.$chunk.'}';
            $began_context = False;
        } else if ($began_context && $chunk == '{') {
            $began_context = False;
            $string .= $chunk;
        } else {
            if (in_array($chunk, $context_triggers)) {
                $began_context = True;
                $context_depth += 1;
            }
            $string .= $chunk;
        }
    }
    return $string;
}

function normalize($latex){
    return chunks_to_string(chunk_math($latex));
}

?>
<?php
/**
 * Author: Archer Reilly
 * Date: 23/Sep/2014
 * File: index.php
 * Desc: the main index file
 *
 * Produced By CSRGXTU.
 */
include('./netlib.php');

$DOMAIN = 'http://csrgxtu.sinaapp.com';
$API = 'http://64.15.119.167//';

if (count($_GET) != 0) {
  // with url parameters
  $data = get_data($API . 'search?q=' . $_GET['q']);
  if ($data == FALSE) {
    // TO-DO
    echo "Exception no data";
  } else {
    $data = str_replace('"/search"', '"' . $DOMAIN . '/index.php"', $data);
    echo $data;
  }
} else {
  // without
  $data = get_data($API);
  if ($data == FALSE) {
    // TO-DO
    echo "Exception no data";
  } else {
    $data = str_replace('"/search"', '"' . $DOMAIN . '/index.php"', $data);
    $data = str_replace('background:url(/images/srpr/logo11w.png)', 'background:url(' . $API . 'images/srpr/logo11w.png)', $data);
    $data = str_replace('"/images/google_favicon_128.png"', '"./google_favicon_128.png"', $data);
    echo $data;
  }
}
?>

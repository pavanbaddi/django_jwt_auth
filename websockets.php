<?php

require_once('./vendor/autoload.php');

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

function d_log( $d ){
    error_log($d, 3, "C:/laragon/www/test_django_js/error.log");
}

function get_request_headers( $data ){
    $headers = array();
    $lines = preg_split("/\r\n/", $data);
    foreach ($lines as $line) {
        $line = chop($line);
        if (preg_match('/\A(\S+): (.*)\z/', $line, $matches)) {
            $headers[$matches[1]] = $matches[2];
        }
    }
    return $headers;
}

function get_cookie_value( $key, $request_data ){
    $cookie_value="";
    $headers = get_request_headers( $request_data );
    $cookie_arr = explode("; ", $headers["Cookie"] ?? "NA" );

    if( is_array($cookie_arr ) && count($cookie_arr ) > 0 ){
        foreach ($cookie_arr  as $key => $item) {
            # code...
            $item_array = explode("=", $item);

            if( is_array( $item_array )  && count($item_array) == 2 && $item_array[0] == $key){
                $cookie_value=$item_array[1];
            }
        }
    }
    return $cookie_value;
}

$address = 'localhost';
$port = 12345;



// Create WebSocket.
$server = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_set_option($server, SOL_SOCKET, SO_REUSEADDR, 1);
socket_bind($server, $address, $port);
socket_listen($server);
$client = socket_accept($server);

// Send WebSocket handshake headers.
$request = socket_read($client, 5000);
// d_log(get_class_methods($client));
// d_log(json_encode(http_parse_headers($request)));
// d_log( json_encode(get_request_headers( $request )));
// d_log($request);

preg_match('#Sec-WebSocket-Key: (.*)\r\n#', $request, $matches);
$key = base64_encode(pack(
    'H*',
    sha1($matches[1] . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
));
$headers = "HTTP/1.1 101 Switching Protocols\r\n";
$headers .= "Upgrade: websocket\r\n";
$headers .= "Connection: Upgrade\r\n";
$headers .= "Sec-WebSocket-Version: 13\r\n";
$headers .= "Sec-WebSocket-Accept: $key\r\n\r\n";
socket_write($client, $headers, strlen($headers));

// Send messages into WebSocket in a loop.

while (true) {
    sleep(1);
    $cookie_string_data = get_cookie_value("token", $request);
    
    $decoded = JWT::decode($cookie_string_data, new Key("secret123", 'HS256'));
    // d_log(gettype($decoded));
    // d_log(json_encode($decoded));
    $username = is_object($decoded) ? $decoded->username : "unauthenticated";
    
    
    $content = 'Now: ' . time();
    $content = 'Token: '.$username;
    $response = chr(129) . chr(strlen($content)) . $content;
    socket_write($client, $response);
}
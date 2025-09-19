<?php
require 'vendor/autoload.php';

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

// Create a new Guzzle client
$client = new Client();

// Define the API endpoint URL
$url = $BASE_URL+'/accounts/token/';

// Define the request body as a PHP array
$data = [
    'username' => 'admin',
    'password' => 'admin'
];

try {
    // Send the POST request with the JSON data
    $response = $client->post($url, [
        'json' => $data
    ]);

    // Get the status code and response body
    $statusCode = $response->getStatusCode();

    echo "Status Code: {$statusCode}\n";

} catch (RequestException $e) {
    // Handle request errors
    echo "Error: " . $e->getMessage() . "\n";
    if ($e->hasResponse()) {
        echo "Response: " . $e->getResponse()->getBody()->getContents() . "\n";
    }
}
?>

<?php
$type = $argv[1] ?? "echo";
$message = $argv[2] ?? "test message";

$request = [
    "type" => $type,
    "message" => $message,
    "sent_at" => date(DATE_ATOM),
];

try {
    require_once __DIR__ . "/rabbitMQLib.inc";

    $client = new rabbitMQClient(__DIR__ . "/testRabbitMQ.ini");
    $response = $client->send_request($request);

    echo "Client received response:" . PHP_EOL;
    print_r($response);
} catch (Throwable $error) {
    error_log("RabbitMQ client sample failed: " . $error->getMessage());
    fwrite(STDERR, "Client error: " . $error->getMessage() . PHP_EOL);
    exit(1);
}

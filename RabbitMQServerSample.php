<?php
function request_processor(array $request): array
{
    if (!isset($request["type"])) {
        return [
            "status" => "error",
            "message" => "Request is missing a type",
        ];
    }

    switch ($request["type"]) {
        case "echo":
            return handle_echo_request($request);

        case "ping":
            return handle_ping_request($request);

        default:
            return handle_unsupported_request($request);
    }
}

// To aid group work, these handler functions can be defined in separate files and included/required in this router-like file.
function handle_echo_request(array $request): array
{
    return [
        "status" => "ok",
        "message" => "Echo: " . ($request["message"] ?? ""),
        "received_at" => date(DATE_ATOM),
    ];
}

function handle_ping_request(array $request): array
{
    return [
        "status" => "ok",
        "message" => "pong",
        "received_at" => date(DATE_ATOM),
    ];
}

function handle_unsupported_request(array $request): array
{
    return [
        "status" => "error",
        "message" => "Unsupported request type: " . $request["type"],
    ];
}

try {
    require_once __DIR__ . "/rabbitMQLib.inc";

    $server = new rabbitMQServer(__DIR__ . "/testRabbitMQ.ini");
    echo "RabbitMQ server sample starting" . PHP_EOL;
    $server->process_requests("request_processor");
} catch (Throwable $error) {
    error_log("RabbitMQ server sample failed: " . $error->getMessage());
    fwrite(STDERR, "Server error: " . $error->getMessage() . PHP_EOL);
    exit(1);
}

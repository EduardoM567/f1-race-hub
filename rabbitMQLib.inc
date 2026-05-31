<?php
use PhpAmqpLib\Channel\AMQPChannel;
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Exception\AMQPTimeoutException;
use PhpAmqpLib\Message\AMQPMessage;

$autoload = __DIR__ . "/vendor/autoload.php";
if (!is_file($autoload)) {
    throw new RuntimeException("Missing Composer dependencies. Run `composer install` before using the RabbitMQ sample.");
}
require_once $autoload;

function loadRabbitMQConfig(string $configFile): array
{
    if (!is_file($configFile)) {
        throw new RuntimeException("RabbitMQ config file not found: {$configFile}");
    }

    $config = parse_ini_file($configFile);
    if ($config === false) {
        throw new RuntimeException("RabbitMQ config file could not be parsed: {$configFile}");
    }

    $required = ["BROKER_HOST", "BROKER_PORT", "USER", "PASSWORD", "VHOST", "QUEUE"];
    foreach ($required as $key) {
        if (!isset($config[$key]) || $config[$key] === "") {
            throw new RuntimeException("RabbitMQ config is missing {$key}");
        }
    }

    $config["BROKER_PORT"] = (int) $config["BROKER_PORT"];
    $config["RESPONSE_TIMEOUT"] = isset($config["RESPONSE_TIMEOUT"])
        ? (int) $config["RESPONSE_TIMEOUT"]
        : 10;

    return $config;
}

function rabbitMQUsesConfiguredExchange(array $config): bool
{
    return isset($config["EXCHANGE"]) && $config["EXCHANGE"] !== "";
}

function rabbitMQRoutingKey(array $config): string
{
    return isset($config["ROUTING_KEY"]) && $config["ROUTING_KEY"] !== ""
        ? $config["ROUTING_KEY"]
        : $config["QUEUE"];
}

function rabbitMQPrepareMessageRoute(AMQPChannel $channel, array $config): void
{
    $queue = $config["QUEUE"];
    $channel->queue_declare($queue, false, false, false, true);

    if (!rabbitMQUsesConfiguredExchange($config)) {
        return;
    }

    $exchange = $config["EXCHANGE"];
    $exchangeType = $config["EXCHANGE_TYPE"] ?? "direct";
    $routingKey = rabbitMQRoutingKey($config);

    $channel->exchange_declare($exchange, $exchangeType, false, false, true);
    $channel->queue_bind($queue, $exchange, $routingKey);
}

function rabbitMQPublishMessage(AMQPChannel $channel, array $config, AMQPMessage $message): void
{
    if (rabbitMQUsesConfiguredExchange($config)) {
        $channel->basic_publish($message, $config["EXCHANGE"], rabbitMQRoutingKey($config));
        return;
    }

    $channel->basic_publish($message, "", $config["QUEUE"]);
}

class rabbitMQServer
{
    private array $config;
    /** @var callable|null */
    private $callback = null;
    private ?AMQPChannel $channel = null;

    public function __construct(string $configFile = "testRabbitMQ.ini")
    {
        $this->config = loadRabbitMQConfig($configFile);
    }

    private function get_connection(): AMQPStreamConnection
    {
        return new AMQPStreamConnection(
            $this->config["BROKER_HOST"],
            $this->config["BROKER_PORT"],
            $this->config["USER"],
            $this->config["PASSWORD"],
            $this->config["VHOST"]
        );
    }

    public function process_requests(callable $callback): void
    {
        $connection = $this->get_connection();
        $channel = $connection->channel();
        $queue = $this->config["QUEUE"];
        $this->callback = $callback;
        $this->channel = $channel;

        rabbitMQPrepareMessageRoute($channel, $this->config);
        $channel->basic_qos(null, 1, null);

        echo "RabbitMQ server listening on queue '{$queue}'" . PHP_EOL;

        $channel->basic_consume(
            $queue,
            "",
            false,
            false,
            false,
            false,
            [$this, "process_message"]
        );

        while ($channel->is_consuming()) {
            $channel->wait();
        }
    }

    public function process_message(AMQPMessage $message): void
    {
        if ($this->callback === null || $this->channel === null) {
            throw new RuntimeException("RabbitMQ server process_message called before process_requests initialized the callback");
        }

        $response = $this->handle_message($message, $this->callback);

        $replyTo = $message->get("reply_to");
        if ($replyTo) {
            $this->channel->basic_publish(
                new AMQPMessage(
                    json_encode($response),
                    [
                        "content_type" => "application/json",
                        "correlation_id" => $message->get("correlation_id"),
                    ]
                ),
                "",
                $replyTo
            );
        }

        $message->ack();
    }

    private function handle_message(AMQPMessage $message, callable $callback): array
    {
        $request = json_decode($message->getBody(), true);
        if (!is_array($request)) {
            error_log("RabbitMQ server received invalid JSON: " . $message->getBody());
            return [
                "status" => "error",
                "message" => "Invalid JSON request",
            ];
        }

        echo "Received request:" . PHP_EOL;
        print_r($request);

        try {
            $response = $callback($request);
            if (!is_array($response)) {
                return [
                    "status" => "ok",
                    "data" => $response,
                ];
            }
            return $response;
        } catch (Throwable $error) {
            error_log("RabbitMQ server callback failed: " . $error->getMessage());
            return [
                "status" => "error",
                "message" => $error->getMessage(),
            ];
        }
    }
}

class rabbitMQClient
{
    private array $config;

    public function __construct(string $configFile = "testRabbitMQ.ini")
    {
        $this->config = loadRabbitMQConfig($configFile);
    }

    private function get_connection(): AMQPStreamConnection
    {
        return new AMQPStreamConnection(
            $this->config["BROKER_HOST"],
            $this->config["BROKER_PORT"],
            $this->config["USER"],
            $this->config["PASSWORD"],
            $this->config["VHOST"]
        );
    }

    public function send_request(array $request): array
    {
        $connection = $this->get_connection();
        $channel = $connection->channel();
        $queue = $this->config["QUEUE"];
        $timeout = $this->config["RESPONSE_TIMEOUT"];
        $correlationId = bin2hex(random_bytes(12));
        $responseBody = null;

        rabbitMQPrepareMessageRoute($channel, $this->config);
        [$callbackQueue] = $channel->queue_declare("", false, false, true, true);

        $channel->basic_consume(
            $callbackQueue,
            "",
            false,
            true,
            false,
            false,
            function (AMQPMessage $message) use ($correlationId, &$responseBody): void {
                if ($message->get("correlation_id") === $correlationId) {
                    $responseBody = $message->getBody();
                }
            }
        );

        $message = new AMQPMessage(
            json_encode($request),
            [
                "content_type" => "application/json",
                "correlation_id" => $correlationId,
                "reply_to" => $callbackQueue,
            ]
        );

        echo "Sending request to queue '{$queue}'" . PHP_EOL;
        rabbitMQPublishMessage($channel, $this->config, $message);

        try {
            while ($responseBody === null) {
                $channel->wait(null, false, $timeout);
            }
        } catch (AMQPTimeoutException $error) {
            error_log("RabbitMQ client timed out waiting for response: " . $error->getMessage());
            throw new RuntimeException("Timed out waiting for RabbitMQ response after {$timeout} seconds");
        } finally {
            $channel->close();
            $connection->close();
        }

        $response = json_decode($responseBody, true);
        if (!is_array($response)) {
            error_log("RabbitMQ client received invalid JSON response: " . $responseBody);
            throw new RuntimeException("RabbitMQ response was not valid JSON");
        }

        return $response;
    }

    public function publish(array $message): void
    {
        $connection = $this->get_connection();
        $channel = $connection->channel();
        rabbitMQPrepareMessageRoute($channel, $this->config);
        rabbitMQPublishMessage(
            $channel,
            $this->config,
            new AMQPMessage(json_encode($message), ["content_type" => "application/json"])
        );

        $channel->close();
        $connection->close();
    }
}

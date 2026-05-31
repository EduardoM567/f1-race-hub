# IT490-2026

Revamp workspace for IT490 Systems Integration starter code, examples, and topic planning.

## RabbitMQ Sample

This repo includes a simplified version of the old IT490 RabbitMQ PHP sample:

- `RabbitMQClientSample.php`
- `RabbitMQServerSample.php`
- `rabbitMQLib.inc`
- `testRabbitMQ.ini`

The sample keeps the old request/response shape:

1. Start the server in one terminal.
2. Run the client in another terminal.
3. The client publishes JSON to a RabbitMQ queue.
4. The server processes the request by `type`.
5. The server sends a JSON response back to the client's callback queue.

Install dependencies:

```sh
composer install
```

Start the server:

```sh
php RabbitMQServerSample.php
```

Send an echo request:

```sh
php RabbitMQClientSample.php echo "hello from IT490"
```

Send a ping request:

```sh
php RabbitMQClientSample.php ping
```

If RabbitMQ is not running or the config is wrong, the sample should throw an error and write a useful message with `error_log`.

## Optional Exchange Routing

The default sample publishes directly to the queue through RabbitMQ's default exchange. That keeps the first echo/ping example focused on the request and response flow.

For exploration, `rabbitMQLib.inc` also supports a named exchange and routing key. Uncomment the optional values in `testRabbitMQ.ini`:

```ini
EXCHANGE=it490_requests
EXCHANGE_TYPE=direct
ROUTING_KEY=sample.request
```

With those values enabled, the library declares the exchange, binds `QUEUE` to it with `ROUTING_KEY`, and publishes requests through the named exchange. This is useful later when a project has separate DB, API, logging, or worker queues.

<?php
//Owner: Ruchir Patel rkp28

#lets PHP know about the RabbitMQ library
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;

#passes on env values
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();

define('MQ_HOST', $_ENV['MQ_HOST']);
define('MQ_PORT', (int) $_ENV['MQ_PORT']);
define('MQ_USER', $_ENV['MQ_USER']);
define('MQ_PASS', $_ENV['MQ_PASS']);
define('MQ_VHOST', $_ENV['MQ_VHOST']);
define('LOG_EXCHANGE', $_ENV['LOG_EXCHANGE']);
define('LOG_ROUTING_KEY', $_ENV['LOG_ROUTING_KEY']);
define('DLQ_QUEUE', $_ENV['DLQ_QUEUE']);

#opens rabbitmq connection
function get_mq_connection(){
    return new AMQPStreamConnection(MQ_HOST, MQ_PORT, MQ_USER, MQ_PASS, MQ_VHOST);
}

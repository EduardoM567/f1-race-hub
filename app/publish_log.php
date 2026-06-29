<?php
# Owner: Ruchir Patel rkp28
require_once __DIR__ . '/log_config.php';
require_once __DIR__ . '/route_dlq.php';

use PhpAmqpLib\Message\AMQPMessage;

#main logging function takes log level and message
function publish_log(string $type, string $message):void{
    $allowed = ['info', 'warning', 'error'];

    #check if message is valid before sending if not sends to DLQ
    if(empty($type) || empty($message) || !in_array($type, $allowed)){
        error_log("[APP-LOGGER] bad log event, sending to DLQ");
        route_to_dlq(['type' => $type, 'message' => $message]);
        return;
    }

    #makes the json message
    $payload = json_encode([
        'source' => gethostname(),
        'timestamp' => date('Y-m-d\TH:i:s'),
        'level' => strtoupper($type),
        'message' => $message
    ]);

    try{
        #reopens channel and connection again
        $conn=get_mq_connection();
        $ch=$conn->channel();

        # makes the exchange  
        $ch->exchange_declare(LOG_EXCHANGE, 'direct', false, true, false);

        #wraps playload in a message
        $msg=new AMQPMessage($payload,[
            'content_type' => 'application/json',
            'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT
        ]);

        #sends to the echange with the routing key
        $ch->basic_publish($msg, LOG_EXCHANGE, LOG_ROUTING_KEY);
        echo "[APP-LOGGER] sent: $payload\n";

        #closes channel and connection
        $ch->close();
        $conn->close();

    
    }catch(Exception $e){
        # if any error happesn during the logging process goes into here and to DLQ
        error_log("[APP-LOGGER] failed to send: " . $e->getMessage());
        route_to_dlq(['type' => $type, 'message' => $message]);
    }
}

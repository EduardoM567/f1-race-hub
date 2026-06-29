<?php
# Owner: Ruchir Patel rkp28

#passes env values from log config
require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

#sends bad messages to DLQ queue
function route_to_dlq(array $data):void{
    try{
        #opens connection to rabbitmq and makes channel
        $conn= get_mq_connection();
        $ch= $conn->channel();

        #make sure dlq exists
        $ch->queue_declare(DLQ_QUEUE, false, true, false, false);

        #make json to send 
        $payload= json_encode([
            'source' => gethostname(),
            'error' => 'malformed_message',
            'data' => $data,
            'timestamp' => date('Y-m-d H:i:s')
        ]);

        #sends json into a RabbitMQ message
        $msg= new AMQPMessage($payload, [
            'content_type' => 'application/json',
            'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT
        ]);

        $ch->basic_publish($msg, '', DLQ_QUEUE);
        echo "[APP-LOGGER] sent to DLQ: $payload\n";

        #closes connection and channel
        $ch->close();
        $conn->close();

    #if error happens this catches it
    }catch(Exception $e){
        error_log("[APP-LOGGER] dlq failed: " . $e->getMessage());
    }
}

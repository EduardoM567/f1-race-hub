<?php
//Owner: Ruchir Patel rkp28

require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

if (empty($_POST['item_id']) || empty($_POST['item_type'])) {
    header("Location: fav.php");
    exit;
}

$user_id = $_SESSION['user_id'];
$item_id = $_POST['item_id'];
$item_type = $_POST['item_type'];

$corrId = uniqid();
$payload = json_encode([
    'type' => 'remove',
    'user_id' => $user_id,
    'item_id' => $item_id,
    'item_type' => $item_type,
    'correlation_id' => $corrId,
    'source' => gethostname(),
    'timestamp' => date('Y-m-d H:i:s')
]);

$conn = get_mq_connection();
$ch = $conn->channel();
$ch->exchange_declare('fav_exchange', 'direct', false, true, false);

$replyQueueName = 'fav_reply_queue';
$msg = new AMQPMessage($payload, [
    'content_type' => 'application/json',
    'correlation_id' => $corrId,
    'reply_to' => $replyQueueName
]);

$ch->basic_publish($msg, 'fav_exchange', 'fav.remove');

$maxAttempts = 10;
$attempts = 0;
$response = null;

while(!$response && $attempts < $maxAttempts){
    $result = $ch->basic_get($replyQueueName);
    if($result){
        $data = json_decode($result->body, true);
        if($data['correlation_id'] === $corrId){
            $response = $data;
            $ch->basic_ack($result->delivery_info['delivery_tag']);
        } else {
            $ch->basic_ack($result->delivery_info['delivery_tag']);
        }
    }
    $attempts++;
    usleep(500000);
}

$ch->close();
$conn->close();

header("Location: fav.php");
exit;
?>

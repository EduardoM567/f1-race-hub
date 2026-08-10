<?php
//Owner: Eduardo Maticorena em567 + Ruchir Patel rkp28

require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'admin') {
    header("Location: homepage.php");
    exit;
}

if (empty($_POST['user_id']) || empty($_POST['role'])) {
    $_SESSION['admin_message'] = 'Missing required fields';
    header("Location: admin.php");
    exit;
}

$user_id = $_POST['user_id'];
$role = $_POST['role'];

$corrId = uniqid();
$payload = json_encode([
    'type' => 'update_role',
    'user_id' => $user_id,
    'role' => $role,
    'correlation_id' => $corrId,
    'source' => gethostname(),
    'timestamp' => date('Y-m-d H:i:s')
]);

$conn = get_mq_connection();
$ch = $conn->channel();
$ch->exchange_declare('admin_exchange', 'direct', false, true, false);

$replyQueueName = 'admin_reply_queue';
$msg = new AMQPMessage($payload, [
    'content_type' => 'application/json',
    'correlation_id' => $corrId,
    'reply_to' => $replyQueueName
]);

$ch->basic_publish($msg, 'admin_exchange', 'admin.update_role');

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
        }
    }
    $attempts++;
    usleep(500000);
}

$ch->close();
$conn->close();

$_SESSION['admin_message'] = $response && $response['success'] ? 'Role updated successfully' : ($response['message'] ?? 'Update failed');
header("Location: admin.php");
exit;
?>

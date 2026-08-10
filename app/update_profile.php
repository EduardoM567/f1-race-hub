<?php
//Owner: Ruchir Patel rkp28

require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

$user_id = $_SESSION['user_id'];
$username = !empty($_POST['username']) ? htmlspecialchars(trim($_POST['username'])) : null;
$email = !empty($_POST['email']) ? trim($_POST['email']) : null;
$password = !empty($_POST['password']) ? $_POST['password'] : null;

if (empty($username) || empty($email)) {
    $_SESSION['profile_message'] = 'Username and email are required';
    header("Location: profile.php");
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $_SESSION['profile_message'] = 'Invalid email address';
    header("Location: profile.php");
    exit;
}

$corrId = uniqid();
$payload = json_encode([
    'type' => 'update_profile',
    'user_id' => $user_id,
    'username' => $username,
    'email' => $email,
    'password' => $password,
    'correlation_id' => $corrId,
    'source' => gethostname(),
    'timestamp' => date('Y-m-d H:i:s')
]);

$conn = get_mq_connection();
$ch = $conn->channel();
$ch->exchange_declare('profile_exchange', 'direct', false, true, false);

$replyQueueName = 'profile_reply_queue';
$msg = new AMQPMessage($payload, [
    'content_type' => 'application/json',
    'correlation_id' => $corrId,
    'reply_to' => $replyQueueName
]);

$ch->basic_publish($msg, 'profile_exchange', 'profile.update');

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

if($response && $response['success']){
    $_SESSION['profile_message'] = 'Profile updated successfully';
} else {
    $_SESSION['profile_message'] = $response['message'] ?? 'Update failed. Please try again.';
}

header("Location: profile.php");
exit;
?>

<?php
//Owner: Ruchir Patel rkp28

require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

$corrId = uniqid();
$payload = json_encode([
    'type' => 'get_news',
    'correlation_id' => $corrId,
    'source' => gethostname(),
    'timestamp' => date('Y-m-d H:i:s')
]);

$conn = get_mq_connection();
$ch = $conn->channel();
$ch->exchange_declare('f1_exchange', 'direct', false, true, false);

$replyQueueName = 'f1_reply_queue';
$msg = new AMQPMessage($payload, [
    'content_type' => 'application/json',
    'correlation_id' => $corrId,
    'reply_to' => $replyQueueName
]);

$ch->basic_publish($msg, 'f1_exchange', 'f1.request');

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

var_dump($_SESSION);

$ch->close();
$conn->close();
?>

<html>
<head>
    <title>F1 News</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>
<h1> F1 News </h1>

<?php if($response && $response['success'] && !empty($response['data'])): ?>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Headlines</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach($response['data'] as $article): ?>
            <tr>
                <td>
                    <a href='<?php echo htmlspecialchars($article['link'] ?? '#'); ?>'>
                        <?php echo htmlspecialchars($article['title'] ?? 'N/A'); ?>
                    </a>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php elseif($response && !$response['success']): ?>
    <p>Error loading news: <?php echo htmlspecialchars($response['message']); ?></p>
<?php else: ?>
    <p>No news available or request timed out.</p>
<?php endif; ?>

</body>
</html>

<?php
//Owner: Ruchir Patel rkp28

date_default_timezone_set('America/New_York');
require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

$corrId = uniqid();
$payload = json_encode([
    'type' => 'get_schedule',
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

$ch->close();
$conn->close();
?>

<html>
<head>
    <title>F1 Race Schedule</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>
<h1>F1 Race Schedule</h1>

<?php if($response && $response['success'] && !empty($response['data'])): ?>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Race Type</th>
                <th>Date</th>
                <th>Location</th>
                <th>Favorite</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach($response['data'] as $race): ?>
            <tr>
                <td>
                    <a href='race_results.php?session_key=<?php echo urlencode($race['session_key'])?>'>
                        <?php echo htmlspecialchars($race['session_name'] ?? 'N/A'); ?>
                    </a>
                </td>
                <td><?php echo date('Y-m-d h:i:s a', strtotime($race['date_start']));?></td>
                <td><?php  echo htmlspecialchars(($race['country_name']) . '-' . ($race['circuit_short_name']));?></td>
                <td>
                <form action="save_fav.php" method="POST">
                <input type="hidden" name="item_id" value="<?php echo htmlspecialchars($race['session_key'] ??  ''); ?>">
                <input type="hidden" name="item_name" value="<?php echo htmlspecialchars(($race['country_name']) . '-' . ($race['circuit_short_name'])); ?>">
                <input type="hidden" name="item_type" value="race">
                <input type="hidden" name="list_name" value="My Favorites">
                <input type="submit" value="★">
                </form>            
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php elseif($response && !$response['success']): ?>
    <p>Error loading schedule: <?php echo htmlspecialchars($response['message']); ?></p>
<?php else: ?>
    <p>No schedule data available or request timed out.</p>
<?php endif; ?>

</body>
</html>

<!-- #Owner: Ruchir Patel rkp28 -->
<?php
require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

$corrId = uniqid();
$payload = json_encode([
    'type' => 'get_standings',
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
    <title>Standings and Roster</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>
<h1>F1 Championship Standing & Roster </h1>

<?php if($response && $response['success'] && !empty($response['data'])): ?>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Position</th>
                <th>Photo</th>
                <th>Driver</th>
                <th>Team</th>
                <th>Points</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach($response['data'] as $driver): ?>
            <tr>
                <td><?php echo htmlspecialchars($driver['position'] ?? 'N/A'); ?></td>
                <td><img src="<?php echo htmlspecialchars($driver['headshot_url'] ?? ''); ?>" alt="" width='80'></td>
                <td><a href='driver.php?driver_number=<?php echo $driver['driver_number']; ?>'>
                    <?php echo $driver['full_name']; ?>
                    </a>
                </td>
                <td><?php echo htmlspecialchars($driver['team_name'] ?? 'N/A'); ?></td>
                <td><?php echo htmlspecialchars($driver['points'] ?? 'N/A'); ?></td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php elseif($response && !$response['success']): ?>
    <p>Error loading Standings and Roster: <?php echo htmlspecialchars($response['message']); ?></p>
<?php else: ?>
    <p>No standings and driver data available or request timed out.</p>
<?php endif; ?>

</body>
</html>

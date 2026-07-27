<!-- #Owner: Ruchir Patel rkp28 -->
<?php
require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

$driver_num= $_GET['driver_number'] ?? null;
if(!$driver_num){
    echo "driver number not reachable";
    exit;
}

$corrId = uniqid();
$payload = json_encode([
    'type' => 'get_driver',
    'params' => ['driver_number' => $driver_num],
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
    <title>F1 Drivers</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>

<h1>Driver Info </h1>

<?php if($response && $response['success'] && !empty($response['data'])): 
    $driver= $response['data'];
    ?>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Photo</th>
                <th>Driver</th>
                <th>Driver Number</th>
                <th>Team</th>
                <th>Points this Season</th>
                <th>Championship Position</th>
                <th>Favorite</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><img src="<?php echo htmlspecialchars($driver['headshot_url'] ?? ''); ?>" alt="" width='100'></td>
                <td><?php echo htmlspecialchars($driver['full_name'] ?? 'N/A')  ?></td>                
                <td><?php echo htmlspecialchars($driver['driver_number'] ?? 'N/A')  ?></td>                
                <td><?php echo htmlspecialchars($driver['team_name'] ?? 'N/A'); ?></td>
                <td><?php echo htmlspecialchars($driver['points'] ?? 'N/A'); ?></td>                
                <td><?php echo htmlspecialchars($driver['position'] ?? 'N/A'); ?></td>
                <td>
                <form action="save_fav.php" method="POST">
                <input type="hidden" name="item_id" value="<?php echo htmlspecialchars($driver['driver_number'] ??  ''); ?>">
                <input type="hidden" name="item_name" value="<?php echo htmlspecialchars($driver['full_name'] ??  ''); ?>">
                <input type="hidden" name="item_type" value="driver">
                <input type="hidden" name="list_name" value="My Favorites">
                <input type="submit" value="★">
                </form>            
                </td>                
            </tr>
        </tbody>
    </table>
<?php elseif($response && !$response['success']): ?>
    <p>Error loading schedule: <?php echo htmlspecialchars($response['message']); ?></p>
<?php else: ?>
    <p>No schedule data available or request timed out.</p>
<?php endif; ?>

</body>
</html>

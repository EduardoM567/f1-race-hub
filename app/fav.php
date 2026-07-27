<!-- #Owner: Ruchir Patel rkp28 -->
<?php
require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}

$user_id = $_SESSION['user_id'];

$corrId = uniqid();
$payload = json_encode([
    'type' => 'view',
    'user_id' => $user_id,
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

$ch->basic_publish($msg, 'fav_exchange', 'fav.view');

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
    <title>My Favorites</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>

<h1>My Favorites - <?php echo htmlspecialchars($_SESSION['username']); ?></h1>

<?php if($response && $response['success'] && !empty($response['data'])): ?>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Name</th>
                <th>Kind</th>
                <th>List</th>
                <th>Unsave</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach($response['data'] as $fav): ?>
            <tr>
                <td><?php echo htmlspecialchars($fav[5]); ?></td>
                <td><?php echo htmlspecialchars($fav[4]); ?></td>
                <td><?php echo htmlspecialchars($fav[2]); ?></td>
                <td>
                    <form action="remove_fav.php" method="POST">
                        <input type="hidden" name="user_id" value="<?php echo htmlspecialchars($user_id); ?>">
                        <input type="hidden" name="item_id" value="<?php echo htmlspecialchars($fav[3]); ?>">
                        <input type="hidden" name="item_type" value="<?php echo htmlspecialchars($fav[4]); ?>">
                        <input type="submit" value="❌">
                    </form>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php elseif($response && !$response['success']): ?>
    <p>Error loading favorites: <?php echo htmlspecialchars($response['message']); ?></p>
<?php else: ?>
    <p>No favorites saved yet.</p>
<?php endif; ?>

</body>
</html>

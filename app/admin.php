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

$corrId = uniqid();
$payload = json_encode([
    'type' => 'get_users',
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

$ch->basic_publish($msg, 'admin_exchange', 'admin.get_users');

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
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>

<h1>Admin Dashboard</h1>

<?php if(isset($_SESSION['admin_message'])): ?>
    <p style="color:#00cc44; padding:10px 30px;"><?php echo htmlspecialchars($_SESSION['admin_message']); unset($_SESSION['admin_message']); ?></p>
<?php endif; ?>

<?php if($response && $response['success'] && !empty($response['data'])): ?>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach($response['data'] as $user): ?>
            <tr>
                <td><?php echo htmlspecialchars($user['username'] ?? 'N/A'); ?></td>
                <td><?php echo htmlspecialchars($user['email']); ?></td>
                <td><?php echo htmlspecialchars($user['role']); ?></td>
                <td><?php echo htmlspecialchars($user['account_status']); ?></td>
                <td style="white-space:nowrap;">
                    <form action="admin_update_role.php" method="POST" style="display:inline;">
                        <input type="hidden" name="user_id" value="<?php echo $user['user_id']; ?>">
                        <select name="role" style="padding:3px 6px; font-size:12px; background-color:#1a1a1a; color:#fff; border:1px solid #444;">
                            <option value="user" <?php echo $user['role'] === 'user' ? 'selected' : ''; ?>>User</option>
                            <option value="admin" <?php echo $user['role'] === 'admin' ? 'selected' : ''; ?>>Admin</option>
                        </select>
                        <input type="submit" value="Update Role" style="padding:3px 8px; font-size:11px; margin-left:4px;">
                    </form>
                    <form action="admin_update_status.php" method="POST" style="display:inline; margin-left:6px;">
                        <input type="hidden" name="user_id" value="<?php echo $user['user_id']; ?>">
                        <input type="hidden" name="current_status" value="<?php echo htmlspecialchars($user['account_status']); ?>">
                        <input type="submit" 
                            value="<?php echo $user['account_status'] === 'active' ? 'Disable' : 'Reactivate'; ?>"
                            style="padding:3px 8px; font-size:11px; background-color:<?php echo $user['account_status'] === 'active' ? '#cc0000' : '#006600'; ?>;">
                    </form>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php elseif($response && !$response['success']): ?>
    <p>Error: <?php echo htmlspecialchars($response['message']); ?></p>
<?php else: ?>
    <p>No users found or request timed out.</p>
<?php endif; ?>

</body>
</html>

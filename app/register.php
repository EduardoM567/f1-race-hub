<!-- #Owner: Ruchir Patel rkp28 -->
<?php
session_start();
$error_message = '';
$success_message = '';

require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

if (!empty($_POST['email']) && !empty($_POST['password']) && !empty($_POST['username'])){
    $email = htmlspecialchars($_POST['email']);
    $password = $_POST['password'];
    $username = htmlspecialchars($_POST['username']);

    $email = filter_var($email, FILTER_SANITIZE_EMAIL);

    if (filter_var($email, FILTER_VALIDATE_EMAIL)){

        $corrId = uniqid();
        $payload = json_encode([
            'type' => 'register',
            'username' => $username,
            'email' => $email,
            'password' => $password,
            'correlation_id' => $corrId,
            'source' => gethostname(),
            'timestamp' => date('Y-m-d H:i:s')
        ]);

        $conn = get_mq_connection();
        $ch = $conn->channel();
        $ch->exchange_declare('auth_exchange', 'direct', false, true, false);

        $replyQueueName = 'auth_reply_queue';
        $msg = new AMQPMessage($payload, [
            'content_type' => 'application/json',
            'correlation_id' => $corrId,
            'reply_to' => $replyQueueName
        ]);

        $ch->basic_publish($msg, 'auth_exchange', 'auth.register');

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

        if($response){
            if($response['success'] === true){
                header("Location: login.php?registered=1");
                exit;
            } else {
                $error_message = $response['message'] ?? 'Registration failed';
            }
        } else {
            $error_message = 'Registration failed - could not reach server';
        }

    } else {
        $error_message = 'Invalid email address';
    }
} elseif (!empty($_POST)) {
    $error_message = 'Please fill in all fields';
}
?>

<html>
<head>
    <title>F1 Race Hub - Register</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

<div style="max-width:400px; margin:80px auto; padding:30px; background-color:#2a2a2a; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.4);">
    <h1 style="color:#e8002d; text-align:center; margin-bottom:24px; font-size:24px;">F1 Race Hub</h1>

    <?php if($error_message): ?>
        <p style="color:#e8002d; text-align:center; margin-bottom:15px;">
            <?php echo htmlspecialchars($error_message); ?>
        </p>
    <?php endif; ?>

    <form action="register.php" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" minlength="4"><br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email"><br><br>
        <label for="pwd">Password:</label>
        <input type="password" id="pwd" name="password" minlength="8"><br><br>
        <input type="submit" value="Register" style="width:100%;">
    </form>
    <p style="text-align:center; margin-top:15px; color:#aaaaaa;">
        Already have an account? <a href="login.php" style="color:#e8002d;">Login here</a>
    </p>
</div>

</body>
</html>

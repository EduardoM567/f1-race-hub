<!-- #Owner: Ruchir Patel rkp28 -->
<?php
session_start();
$error_message = '';

require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

if (!empty($_POST['email']) && !empty($_POST['password'])){
    $email = htmlspecialchars($_POST['email']);
    $password = $_POST['password'];

    $email = filter_var($email, FILTER_SANITIZE_EMAIL);

    if (filter_var($email, FILTER_VALIDATE_EMAIL)){

        $corrId = uniqid();
        $payload = json_encode([
            'type' => 'login',
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

        $ch->basic_publish($msg, 'auth_exchange', 'auth.login');

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
                $_SESSION['user_login'] = 1;
                $_SESSION['username'] = $response['username'];
                $_SESSION['user_id'] = $response['user_id'];
                $_SESSION['role'] = $response['role'] ?? 'user';
                header("Location: homepage.php");
                exit;
            } else {
                $error_message = 'Login failed - invalid email or password';
            }
        } else {
            $error_message = 'Login failed - could not reach server';
        }

    } else {
        $error_message = 'Email is not valid';
    }
} elseif (!empty($_POST)) {
    $error_message = 'Please fill in all fields';
}
?>

<html>
<head>
    <title>F1 Race Hub - Login</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

<div style="max-width:400px; margin:80px auto; padding:30px; background-color:#2a2a2a; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.4);">
    <h1 style="color:#e8002d; text-align:center; margin-bottom:24px; font-size:24px;">F1 Race Hub</h1>

    <?php if(isset($_GET['registered'])): ?>
        <p style="color:#00cc44; text-align:center; margin-bottom:15px;">
            Registration successful! Please login.
        </p>
    <?php endif; ?>

    <?php if($error_message): ?>
        <p style="color:#e8002d; text-align:center; margin-bottom:15px;">
            <?php echo htmlspecialchars($error_message); ?>
        </p>
    <?php endif; ?>

    <form action="login.php" method="POST">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email"><br><br>
        <label for="pwd">Password:</label>
        <input type="password" id="pwd" name="password" minlength="8"><br><br>
        <input type="submit" value="Login" style="width:100%;">
    </form>
    <p style="text-align:center; margin-top:15px; color:#aaaaaa;">
        Don't have an account? <a href="register.php" style="color:#e8002d;">Register here</a>
    </p>
</div>

</body>
</html>

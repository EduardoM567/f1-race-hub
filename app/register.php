<!-- #Owner: Ruchir Patel rkp28 -->
<html>
<body>
<h1>Racing Dev</h1>
<form action="register.php" method="POST">
    <label for="username"><b>Username</label><b>
    <input type="text" id="username" name="username" minlength="4"><br><br>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email"><br><br>
    <label for="pwd">Password:</label>
    <input type="password" id="pwd" name="password" minlength="8"><br><br>
    <input type="submit">
</form>
</body>
</html>

<?php
require_once __DIR__ . '/log_config.php';
use PhpAmqpLib\Message\AMQPMessage;

if (!empty($_POST['email']) && !empty($_POST['password']) && !empty($_POST['username'])){
    $email = htmlspecialchars($_POST['email']);
    $password = ($_POST['password']);
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
            echo $response['message'];
        } else {
            echo "Registration failed - no response received";
        }

    } else {
        echo("$email is not a valid email address");
    }
}
?>

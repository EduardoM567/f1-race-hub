<?php 
//Owner: Ruchir Patel rkp28

session_start(); ?>

<html>
<body>
<h1>Racing Dev</h1>
<form action="login.php" method="POST">
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
                echo 'Login failed - invalid email or password';
            }
        } else {
            echo "Login failed - could not reach server";
        }

    } else {
        echo "Email is not valid.";
    }
} else {
    echo "Please fill in all fields";
}
?>        

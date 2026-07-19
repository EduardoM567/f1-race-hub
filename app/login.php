<!-- #Owner: Ruchir Patel rkp28 -->
<?php
session_start();
?>
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


if (isset($_POST['email']) && isset($_POST['password'])){

    #passes the post data from the form to a php variable
    $email = htmlspecialchars($_POST['email']);

    #passes the password into a php variable 
    $password = ($_POST['password']);
    if (isset($password)) {
    echo "password variable is valid";
    }

    #gets rid of chars not needed or allowed in emails ex.!#/$
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);

    #checks if the email format is valid
    if (filter_var($email, FILTER_VALIDATE_EMAIL)){
        echo("$email is a valid email address");

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
        $msg = new AMQPMessage($payload,[
        'content_type' => 'application/json',
        'correlation_id' => $corrId,
        'reply_to' => $replyQueueName
        ]);

        $ch->basic_publish($msg, 'auth_exchange', 'auth.login');

        $maxAttempts = 10;
        $attempts = 0;
        $response = null;

        while(!$response && $attempts < $maxAttempts){
        $result=$ch->basic_get($replyQueueName);
        if($result){
            $data = json_decode($result->body, true);
            if ($data['correlation_id']===$corrId){
                $response=$data;
                $ch->basic_ack($result->delivery_info['delivery_tag']);
                }
            }
            $attempts++;
            usleep(500000);
        }

        $conn->close();
        $ch->close();

        if($response){
            if ($response['success']===true){
                $_SESSION['user_login'] = 1;
                header("Location: homepage.php");
                exit;
                echo $response['message'];
            }else{
                echo 'Login has failed';
            }
        }else{
            echo "Not able to reach RabbitMQ.";
        }
    }else{
        echo("Email is not valid.");
    }
}
?>

        
<?php
session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
}
echo "you are logged, here is account content";
<?php
session_start();
$_SESSION['user_login'] = 1;
echo "test login successful!";
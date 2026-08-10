<?php
//Owner: Ruchir Patel rkp28

session_start();
session_unset();
session_destroy();
header("Location: login.php");

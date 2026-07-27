<?php
session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
};
?>
<html>
<head>
<link rel="stylesheet" href="css/styles.css">
</head>
<body>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>
hey this is the main content of the site
</body>
</html>


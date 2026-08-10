<?php
//Owner: Ruchir Patel rkp28

session_start();
if (!isset($_SESSION['user_login'])) {
    header("Location: login.php");
    exit;
};
?>
<html>
<?php require_once __DIR__ . '/assets/navbar.php'; ?>

<body>
<h1>Update Profile</h1>
<link rel="stylesheet" href="css/styles.css">
<form action="update_profile.php" method="POST">

    <label for="username"><b>Username:</label><b>
    <input type="text" id="username" name="username" minlength="4" required><br><br>

    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required><br><br>

    <label for="pwd">New Password:</label>
    <input type="password" id="pwd" name="password" minlength="8"> Not Required<br><br>

    <input type="submit">
</form>
</body>
</html>
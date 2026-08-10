<!-- #Owner: Ruchir Patel rkp28 -->

<ul>
    <li><a href="homepage.php">Home</a></li>
    <li><a href="schedule.php">Race Schedule</a></li>
    <li><a href="standings.php">Standings & Roster</a></li>
    <li><a href="fav.php">Favorites</a></li>
    <li><a href="profile.php">Profile</a></li>
    <?php if(isset($_SESSION['role']) && $_SESSION['role'] === 'admin'): ?>
    <li><a href="admin.php">Admin</a></li>
    <?php endif; ?>
    <li><a href="logout.php">Logout</a></li>

    <li class="navbar-home-right">
        <?php echo htmlspecialchars($_SESSION['username']); ?> 
    </li>
</ul>


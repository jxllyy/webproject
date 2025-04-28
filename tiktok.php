<?php
$ip = $_SERVER['REMOTE_ADDR'];
$logFile = 'tiktok_visits.txt';
$currentTime = time();
$redirectToIndex = false;

// Clean up old entries (older than 1 minute)
if (file_exists($logFile)) {
    $visits = file($logFile, FILE_IGNORE_NEW_LINES);
    $newVisits = [];
    foreach ($visits as $visit) {
        list($savedIp, $timestamp) = explode('|', $visit);
        if ($currentTime - $timestamp < 60) {
            $newVisits[] = $visit;
            if ($savedIp === $ip) {
                $redirectToIndex = true;
            }
        }
    }
    file_put_contents($logFile, implode("\n", $newVisits) . "\n");
} else {
    touch($logFile);
}

// Redirect if recent visit detected
if ($redirectToIndex) {
    header('Location: index.html');
    exit;
}

// Record new visit
file_put_contents($logFile, "$ip|$currentTime\n", FILE_APPEND);
?>
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TopFinds</title>
    <link rel="icon" href="logo-squared.jpg" type="image/jpeg">
    <style>
        body {
            background-color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            text-align: center;
        }

        .message {
            font-size: 24px;
            padding: 20px;
            max-width: 80%;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="message">
        For better experience, open this website in browser
    </div>
</body>
</html>
<?php

require_once('bookmarks_fns.php');
session_start();
$old_user=$_SESSION['valid_user'];

unset($_SESSION['valid_user']);
$result_dest=session_destroy();

do_html_header('Logging out');
if(!empty($old_user)){
    if($result_dest){
        echo 'Log Out<br />';
    }
    else{
        echo 'could not log out';
    }
}
else{
    echo 'You are not logged in,and so not have log out.<br />';
    do_html_URL('login.php',Login);
}
do_html_footer();

?>
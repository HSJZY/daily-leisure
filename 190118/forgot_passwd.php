<?php
require_once('bookmarks_fns.php');
do_html_header('Resetting passwd');

$username=$_POST['username'];
try{
    echo "her";
    $password=reset_password($username);
    echo $password."password";
    notify_password($username,$password);
    echo 'your passwd has been emailed to you';
}
catch(Exception $e){
    echo "your password could not be reset";
    echo $e->getMessage();
}
do_html_url('login.php','Login');
do_html_footer();

?>
<?php
require_once('bookmarks_fns.php');
session_start();
if(!isset($_POST['username'])){
    $_POST['username']=" ";
}

if(!isset($_POST['passwd'])){
    $_POST['passwd']=" ";
}
$username=$_POST['username'];
$passwd=$_POST['passwd'];

if($username && $passwd){
    try{
        login($username,$passwd);
        $_SESSION['valid_user']=$username;
    }
    catch(Exception $e){
        do_html_header("Problem");
        echo "you are not logged in, you should log in to view this page";
        echo $e->getMessage();
        do_html_url('login.php','Login');
        do_html_footer();
        exit;
    }
}
do_html_header('Home');
check_valid_user();
if($url_array=get_user_urls($_SESSION['valid_user'])){
    display_user_urls($url_array);
}

display_user_menu();
do_html_footer();
?>
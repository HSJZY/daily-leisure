<?php
require_once('bookmarks_fns.php');
$email=$_POST['email'];
$username=$_POST['username'];
$passwd=$_POST['passwd'];
$passwd2=$_POST['passwd2'];

session_start();

try 
{
    if(!filled_out($_POST)){
        throw new Exception("not filled out");
    }
    if(!valid_email($email)){
        throw new Exception("not correct email");
    }

    if($passwd!==$passwd2){
        throw new Exception("two passwd not same");
    }

    if(strlen($passwd)<6 || strlen($passwd)>16){
        throw new Exception("incorrect length of passwd");
    }
    register($username,$email,$passwd);
    $_SESSION['valid_user']=$username;

    do_html_header("Restration successful");
    echo  "your restration was successful";
    do_html_url("member.php","Go back to member page");
    do_html_footer();
}
catch(Exception $e){
    do_html_header('Problem');
    echo $e->getMessage();
    do_html_footer();
    exit;
}

?>
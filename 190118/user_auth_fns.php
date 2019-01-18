<?php
require_once('db_fns.php');

function register($username,$email,$passwd){
    $conn=db_connect();
    // exit;

    
    $result=$conn->query("select * from user where username='".$username."'");
    if(!$result){
        throw new Exception("could not query database");
    }
    if($result->num_rows>0){
        throw new Exception('That username is taken - go back and choose another one.');
    }
    $result=$conn->query("insert into user values('".$username."', sha1('".$passwd."'), '".$email."')");
    if (!$result) {
        throw new Exception('Could not register you in database - please try again later.');
      }
    return true;
}

function login($username,$passwd){
    $conn=db_connect();
    $result=$conn->query("select * from user where username='".$username."' and passwd=sha1('".$passwd."')");
    if(!$result){
        throw new Exception("could not log you in 1");
    }
    if($result->num_rows>0){
        return true;
    }
    else{
        throw new Exception("could not log you in 2");
    }
}

function check_valid_user(){
    if (isset($_SESSION['valid_user'])){
        echo "log in as ".$_SESSION['valid_user'].".<br/>";
    } else {
        // they are not logged in
        do_html_header('Problem:');
        echo 'You are not logged in.<br/>';
        do_html_url('login.php', 'Login');
        do_html_footer();
        exit;
    }
}

function change_passwd($username,$old_passwd,$new_passwd){
    login($username,$old_passwd);
    $conn=db_connect();
    $result=$conn->query("update user set passwd=sha1('".$new_passwd."') where username='".$username."'");
    if(!$result){
        throw new Exception('Password could not be change');
        return false;
    }else{
        return true;
    }
}

function get_random_word($min_length,$max_length){
    $word="";
    $dictionary="abcdefghigklmnopqrstuvwxyz1234567890_ABCDEFGHIGKLMNOPQRSTUVWXYZ";
    $size_dic=strlen($dictionary);
    $word_size=rand($min_length,$max_length);
    for($i=0;$i<$word_size;$i++){
        $word.=$dictionary[rand(0,$size_dic-1)];
    }
    return $word;
}

function reset_password($username){
    $new_passwd=get_random_word(6,13);
    if($new_passwd==false){
        $new_passwd='ChangeMe';
    }
    $random_num=rand(0,999);
    $new_passwd.=$random_num;

    echo "<br />new passwd:".$new_passwd."<br />";

    $conn=db_connect();
    $result=$conn->query("update user set passwd=sha1('".$new_passwd."') where username='".$username."'");
    if(!$result){
        throw new Exception("Could not change password");
    }
    else{
        return $new_passwd;
    }
}

function notify_password($username,$passwd){
    $conn=db_connect();
    $result=$conn->query("select email from user where username='".$username."'");
    if(!$result){
        throw new Exception("Could not found email address");
    }else if($result->num_rows==0){
        throw new Exception("Could not found email address");
    }
    else{
        $row=$result->fetch_row();
        $email=$row->email;
        $from='1399039408@163.com';
        $mesg="your phpbookmark login password has been changed to ".$passwd."\r\n";
        if(mail($email,'PhP bookmark login information',$mesg)){
            return true;
        }else{
            throw new Exception('Could not send email');
        }
    }
}

?>
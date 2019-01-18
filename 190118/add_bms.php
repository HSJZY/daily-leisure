<?php
    require_once('bookmarks_fns.php');
    session_start();
    $new_url=$_POST['new_url'];
    do_html_header('Adding bookmarks');

    try{
        check_valid_user();
        if(!filled_out($_POST)){
            throw new Exception("Form not complete filledout");
        }

        if(strstr($new_url,'http://')===false){
            $new_url='http://'.$new_url;
        }
        if(!(@fopen($new_url,'r'))){
            throw new Exception("Not a valid url");
        }

        add_bm($new_url);
        echo "Bookmark added.";
        $url_array=get_user_urls($_SESSION['valid_user']);
        if($url_array){
            display_user_urls($url_array);
        }
    }
    catch(Exception $e){
        echo $e->getMessage();
    }
    display_user_menu();
    do_html_footer();
?>
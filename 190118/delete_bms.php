<?php
    require_once('bookmarks_fns.php');
    session_start();
    $del_me=$_POST['del_me'];
    $valid_user=$_SESSION['valid_user'];

    do_html_header('Deleting bookmarks');
    check_valid_user();
    if(!filled_out($_POST)){
        echo 'you have not chosen any bookmarks to delete';
        display_user_menu();
        do_html_footer();
        exit;
    }else{
        if (count($del_me)>0){
            foreach($del_me as $url){
                if(delete_bm($valid_user,$url)){
                    echo "deleted. ".htmlspecialchars($url).'<br />';
                }else{
                    echo "could not delete ".htmlspecialchars($url)."<br />";
                }
            }
        }
        else{
            echo "no bookmarks selected for deletion";
        }
    }
    if($url_array=get_user_urls($valid_user)){
        display_user_urls($valid_user);
    }
    display_user_menu();
    do_html_footer();

?>
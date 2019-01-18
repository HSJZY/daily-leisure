<?php
    require_once("boomarks_fns.php");
    session_start();
    do_html_header();
    try{
        check_valid_user();
        $urls=recomment_urls($_SESSION['valid_user']);
        display_recommended_urls($urls);
    }catch(Exception $e){
        echo $e->getMessage();
    }
    display_user_menu();
    do_html_footer();
?>
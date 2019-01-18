<?php

function filled_out($vars_form){
    foreach($vars_form as $form_key=>$form_val){
        if(!isset($form_key)||!isset($form_val)){
            return false;
        }
    }
    return true;
}

function valid_email($address){
    if(preg_match('/^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$/',$address)){
        return true;
    }
    return false;
}
// echo "hello"; 
// if(valid_email('hnld0923@163.com')==true){
//     echo 'hello';
// }

?>
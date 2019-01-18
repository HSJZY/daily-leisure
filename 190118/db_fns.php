<?php
function db_connect(){
    $result=new mysqli('localhost','zayvin','123456','bookmarks');
    if(!$result){
        throw new Exception('could not connect to database'); 
    }
    else{
        return $result;
    }
}
?>
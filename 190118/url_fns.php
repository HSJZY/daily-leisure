<?php
require_once('db_fns.php');
function get_user_urls($username){
    $conn=db_connect();
    $result=$conn->query("select bm_url from bookmark where username='".$username."'");

    if(!$result){

        return false;
    }
    $url_array=array();
    for($i=0;$row=$result->fetch_row();++$i){
        $url_array[$i]=$row[0];
    }
    return $url_array;
}

function add_bm($new_url){
    echo "attemp to add".htmlspecialchars($new_url)."<br />";
    $valid_user=$_SESSION['valid_user'];
    $conn=db_connect();
    $result=$conn->query("select * from bookmark where username='$valid_user' and bm_url='".$new_url."'");
    if(!$result){
        throw new Exception("Bookmarks already exist");
    }
    
    if(!($conn->query("insert into bookmark values('".$valid_user."','".$new_url."')"))){
        throw new Exception("Bookmarks could not be insert");
    }
    return true;
}

function delete_bm($user,$url){
    $conn=db_connect();
    echo "url:".$url."user:".$user;
    $result=$conn->query("delete from bookmark where bm_url='".$url."' and username='".$user."'");
    if(!$result){
        throw new Exception("Bookmark could not be deleted. "); 
    }else{
        return true;
    }
}

function recommend_urls($valid_user,$popularity){
    $conn=db_connect();
    $query="select bm_url
            from bookmark
            where username in
                (select distinct(b2.username)
                from bookmark b1,bookmark b2
                and b1.username='".$valid_user."'
                and b1.username!=b2.username
                and b1.bm_url=b2.bm_url)
            and bm_url not in
                (select bm_url
                from bookmark
                where username='".$valid_user."')
            group by bm_url
            having count(bm_url)>".$popularity;
    
    if(!$result=$conn->query($query)){
        throw new Exception('could not found any bookmark to recommend');
    }
    if(!$result->num_rows==0){
        throw new Exception('could not found any bookmark to recommend');
    }
    $urls=array();
    for($count=0;$row=$result->fetch_object();$count++){
        $urls[$count]=$row->bm_url;
    }
    return $urls;
            
}

?>
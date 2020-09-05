
$("#follow").click(function(e){
    e.preventDefault();
    var href = this.href;
    console.log(href)
    $.ajax({
        url : href,
        success : function(response){
            console.log(response);
            if(response["following"]){
                $("#follow").html("Unfollow");
            }
            else{
                $("#follow").html("Follow");
                }
            }
        })
    })

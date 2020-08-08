

//Ajax managing like and dislike comment event
$(document).on('click', '#like', function(event){
    event.preventDefault();
    var pk = $(this).attr('value');
    $.ajax({
        type: 'POST',
        url: "{% url 'like_comment' %}",
        data: {'id':pk, 'csrfmiddlewaretoken':'{{ csrf_token }}'},
        dataType: 'json',
        success: function(response){
            console.log($('#like-section').html(response['form']));
            },
            error: function(rs, e){
                console.log(rs.e)
            },
    });
});

//End Ajax like/dislike


//Ajax managing like and dislike feed event
$(document).on('click', '#feedlike', function(event){
    event.preventDefault();
    var pk = $(this).attr('value');
    $.ajax({
        type: 'POST',
        url: "{% url 'like_feed' %}",
        data: {'id':pk, 'csrfmiddlewaretoken':'{{ csrf_token }}'},
        dataType: 'json',
        success: function(response){
            console.log($('#like-feed-section').html(response['form']));
            },
            error: function(rs, e){
                console.log(rs.e)
            },
    });
});
//End Ajax like/dislike
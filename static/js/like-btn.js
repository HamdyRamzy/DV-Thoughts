$(document).ready(function(){ 


    
    $('.like-form').submit(function(e){
        e.preventDefault()
        
        const topic_id = $(this).attr('id');
        
        const likeText = $(`.like-btn${topic_id}`).text()
        const trimedlikeText = $.trim(likeText)
        
        const url = $(this).attr('action');
        
        let result;
        
        const likes = $(`.like-count${topic_id}`).text()
        const trimedlikes = parseInt(likes)
        
        $.ajax({
            type:'POST',
            url:url,
            data:{
                
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'topic_id':topic_id,
            },
            success: function(response) {
                
                if(trimedlikeText === 'Unlike') {
                    $(`.like-btn${topic_id}`).text('Like')
                    result = trimedlikes - 1
                } else {
                    $(`.like-btn${topic_id}`).text('Unlike')
                    result = trimedlikes + 1
                }

                $(`.like-count${topic_id}`).text(result)
            
            },


            error: function(response) {
                    console.log('error', response)
                }


        })     


    })

});
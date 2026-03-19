document.addEventListener('DOMContentLoaded', function() {

    const form = document.querySelector('#comment_form');

    form.addEventListener("submit", submitComment);

    function submitComment(event) {
        event.preventDefault();

        const username = form.querySelector('input[name="username"]').value;
        const comment = form.querySelector('textarea[name="comment"]').value;
        let csrftoken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
        let article_id = form.querySelector('input[name="article_id"]').value;

        if(username && comment) {

            console.log(username)
            console.log(comment)
            console.log(csrftoken)

            fetch(`/${article_id}/comments`, {
            method: 'POST',  
                body: JSON.stringify({
                    user: username,
                    content: comment,
                    article_id: article_id
                }), 
                headers: { 'Content-Type':'application/json',
                    'X-CSRFToken': csrftoken, 
                },
            })
            .then(response => { console.log(response); window.location.reload(); })
        }
    }

});
function deleteCom(commentId){
    fetch('/delete-com',{
        method: "POST",
        body: JSON.stringify({commentId: commentId})
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteCom(commentId){
    fetch('/com/delete',{
        method: "POST",
        body: JSON.stringify({commentId: commentId})
    }).then((_res) => {
        location.reload();
    });
}
function deletePatient(patientId){
    fetch('/patients/delete',{
        method: "POST",
        body: JSON.stringify({patientId: patientId})
    }).then((_res) => {
        location.reload();
    });
}
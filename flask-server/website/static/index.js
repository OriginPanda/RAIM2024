
function deleteCom(commentId){
    fetch('/delete-com',{
        method: "POST",
        body: JSON.stringify({commentId: commentId})
    }).then((_res) => {
        window.location.href = "/";
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
function deleteMed(medicaldataId){
    fetch('/patients/delMed',{
        method: "POST",
        body: JSON.stringify({medicaldataId: medicaldataId})
    }).then((_res) => {
        location.reload();
    });
}


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
function addPatient(patientId){
    fetch('/patients/addPatient',{
        method: "POST",
        body: JSON.stringify({patientId: patientId})
    }).then((_res) => {
        location.reload();
    });
}
function deleteFromMyPatients(patientId){
    fetch('/patients/deleteFromMyPatients',{
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

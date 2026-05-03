// document.getElementById("patientForm").addEventListener("submit", function(e) {
//   e.preventDefault();

//   const formData = new FormData(this);

//   const data = Object.fromEntries(formData.entries());

//   // data.diabetes = this.diabetes.checked ? 1 : 0;
//   // data.hypertension = this.hypertension.checked ? 1 : 0;
//   // data.heart_disease_history = this.heart_disease.checked ? 1 : 0;

//   console.log("FORM DATA:", data);

// //   fetch("YOUR_BACKEND_URL/predict", {
// //   method: "POST",
// //   headers: { "Content-Type": "application/json" },
// //   body: JSON.stringify(data)
// // });
  
//   //go to confirmation page
//   window.location.href = "confirmationScreen.html";
// });

// const data = {
//   first_name,
//   last_name,
//   dob,
//   returning_patient,
//   chest_pain,
//   shortness_of_breath,
//   smoking
// };

// //on submit send data to backend patientIntake and store in local storage + go to confirmation
// fetch("http://127.0.0.1:8000/patientIntake", {
//   method: "POST",
//   headers: { "Content-Type": "application/json" },
//   body: JSON.stringify(data)
// })
// .then(response => response.json())
// .then(result => {
//   localStorage.setItem("patientIntakeData", JSON.stringify(data));
//   window.location.href = "confirmationScreen.html";
// });

document.getElementById("patientForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    //convert string numbers to actual numbers
    data.returning_patient = Number(data.returning_patient);
    data.chest_pain = Number(data.chest_pain);
    data.shortness_of_breath = Number(data.shortness_of_breath);
    data.smoking = Number(data.smoking);

    console.log("PATIENT INTAKE DATA:", data);

    fetch("http://127.0.0.1:8000/patientIntake", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        console.log("BACKEND RESPONSE:", result);

        //store intake data
        //localStorage.setItem("patientIntakeData", JSON.stringify(data));
        // const existingPatientData = JSON.parse(localStorage.getItem("patientIntakeData")) || [];
        // existingPatientData.push(data);
        // localStorage.setItem("patientIntakeData", JSON.stringify(existingPatientData));
        
        // localStorage.setItem("currentPatient", JSON.stringify(data));

        const existing = localStorage.getItem("patientIntakeRecords");
        let existingPatient = [];

        if (existing) {
        const parsed = JSON.parse(existing);
        existingPatient = Array.isArray(parsed) ? parsed : [parsed];
        }

        existingPatient.push(data);

        localStorage.setItem("patientIntakeData", JSON.stringify(existingPatient));
        localStorage.setItem("patientIntakeData", JSON.stringify(data));

        //go to confirmation page
        window.location.href = "confirmationScreen.html";
    })
    .catch(error => {
        console.error("ERROR:", error);
        alert("There was a problem submitting the form.");
    });

});
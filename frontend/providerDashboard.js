document.addEventListener("DOMContentLoaded", function() {

    // if (localStorage.getItem("providerLoggedIn") !== "true") {
    //     window.location.href = "providerDashboard.html";
    //     return;
    // }

    const form = document.getElementById("vitalsForm");
    const patientError = document.getElementById("patientError");
    const patientFound = document.getElementById("patientFound");
    const logoutButton = document.getElementById("logoutButton");

    function getPatient() {
        const data = localStorage.getItem("patientIntakeData");

        if (!data) {
            return [];
        }

        try {
            const parsedData = JSON.parse(data);
            if (Array.isArray(parsedData)) {
                return parsedData; 
            }

            return [parsedData];
        } catch (error) {
            console.error("Error parsing patient intake data:", error);
            return [];
        }
    }


    function findPatientByName(name) {
        const normalizedName = name.trim().toLowerCase();
        return getPatient().find(patient => {
            const fullName = `${patient.first_name} ${patient.last_name}`.toLowerCase();
            return fullName === normalizedName;
        });
    }

    function getRiskClass(category) {
        if (!category) return "";

        const normalized = String(category).toLowerCase();

        if (normalized === "high") return "risk-high";
        if (normalized === "medium") return "risk-medium";
        return "risk-low";
    }

    function renderQueue() {
        const queueBody = document.getElementById("patientQueueBody");
        const queue = JSON.parse(localStorage.getItem("riskQueue")) || [];

        if (queue.length === 0) {
            queueBody.innerHTML = "<tr><td colspan='4'>No patients in queue.</td></tr>";
            return;
        }

        queue.sort((a, b) => b.riskScore - a.riskScore);
        
        queueBody.innerHTML = queue.map((patient, index) => `
            <tr>
                <td>
                <button class="admitButton" onclick="admitPatient(${index})">Admit</button>
                </td>
                <td>${patient.patientName}</td>
                <td>${(Number(patient.riskScore || 0) * 100).toFixed(3)}%</td>
                <td class="${getRiskClass(patient.category)}">${patient.category} </td>
            </tr>
        `).join("");
    }

    
    // function admitPatient(index) {
    //     const confirmAdmit = confirm("Are you sure you want to admit this patient? This action cannot be undone.");
        
    //     if (!confirmAdmit) {
    //         return;
    //     }

    //     const queue = JSON.parse(localStorage.getItem("riskQueue")) || [];
    //     queue.splice(index, 1);

    //     localStorage.setItem("riskQueue", JSON.stringify(queue));
    //     renderQueue();
    // }

    // window.admitPatient = admitPatient;

    let selectedPatientIndex = null;
    function admitPatient(index) {
        selectedPatientIndex = index;
        document.getElementById("admitModal").classList.remove("hidden");
    }

    window.admitPatient = admitPatient;

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        patientError.textContent = "";
        patientFound.textContent = "";

       
       
        const patientID = document.getElementById("patientID").value.trim();
        const patientName = document.getElementById("patientName").value;
        const patient = findPatientByName(patientName);


        // if (!patientID && !findPatientByName(document.getElementById("patientName").value)) {
        //     patientError.textContent = "Patient not found. Please check the name/or verify patient intake was completed.";
        //     return;
        // }

        if (Number(patient.returning_patient) === 1 && !patientID) {
            patientError.textContent = "Returning patient detected. Please enter Patient ID.";
            return;
        }


        if(!patient) {
            patientError.textContent = "Patient not found. Please check the name/or verify patient intake was completed.";
            return;
        }

        patientFound.textContent = `Patient found: ${patient.first_name} ${patient.last_name}`;

        const vitalsData = {
            patient_id: patientID || null,
            elevated_troponin: Number(document.getElementById("elevatedTroponin").value),
            ecg: Number(document.getElementById("ecgAbnormalities").value === "abnormal" ? 1 : 0),
            heart_rate: Number(document.getElementById("heartRate").value)
        };

        const requestBody = {
            patient_intake: patient,
            provider_triage: vitalsData
        };

        fetch("http://127.0.0.1:8000/final-risk-assessment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestBody)
        })
        .then(response => response.json())
        .then(data => {
            const prediction = data.prediction;
            const queue = JSON.parse(localStorage.getItem("riskQueue")) || [];

            queue.push({ patientName: `${patient.first_name} ${patient.last_name}`, 
                          riskScore: Number(prediction.riskScore),
                        category: prediction.category
            });

            queue.sort((a, b) => b.riskScore - a.riskScore);

            localStorage.setItem("riskQueue", JSON.stringify(queue));

            document.getElementById("successMessage").textContent = "Vitals submitted successfully! Patient added to Queue.";

            form.reset();
            patientFound.textContent = "";
            patientError.textContent = "";

            renderQueue();
        })
        .catch(error => {
            console.error("Error submitting vitals:", error);
            patientError.textContent = "Unable to calculate risk score.";
        });

        sessionStorage.setItem("currentPatientVitals", JSON.stringify(vitalsData));
        sessionStorage.setItem("currentPatient", JSON.stringify(patient));

        // alert("Vitals submitted successfully!");
    });

    
    logoutButton.addEventListener("click", function() {
        sessionStorage.removeItem("providerLoggedIn");
        sessionStorage.removeItem("providerUsername");
        window.location.href = "provider.html";
    });

    renderQueue();

    const modal = document.getElementById("admitModal");
    const confirmBtn = document.getElementById("confirmAdmit");
    const cancelBtn = document.getElementById("cancelAdmit");

    confirmBtn.addEventListener("click", function () {
        if (selectedPatientIndex !== null) {
            const queue = JSON.parse(localStorage.getItem("riskQueue")) || [];

            queue.splice(selectedPatientIndex, 1);

            localStorage.setItem("riskQueue", JSON.stringify(queue));
            renderQueue();
        }

        closeModal();
    });

    cancelBtn.addEventListener("click", closeModal);

    function closeModal() {
        modal.classList.add("hidden");
        selectedPatientIndex = null;
    }

});

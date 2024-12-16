// Function to open the modal
function openModal() {
    document.getElementById("uploadModal").style.display = "block";
}

// Function to close the modal
function closeModal() {
    document.getElementById("uploadModal").style.display = "none";
}

// Send file to the backend and handle OCR processing
function sendFileToBackend(file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/uploads", {
        method: "POST",
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Show Image")
            // Display image preview
            if (data.imagePreview) {
                console.log("image in data" + data.imagePreview)
                displayImagePreview(data.imagePreview)
            } else {
                filePreview.innerHTML = "No image preview available.";
            }

            // Display OCR results
            if (data.extractedText) {
                console.log("Show text")
                const jsonData = mapToJSON(data.extractedText);
                displayMappedText(jsonData);

            } else {
                alert("No text was extracted from the image.");
            }

            alert("OCR Process Completed Successfully");
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

// Map extracted text to JSON format
function mapToJSON(text) {
    const filteredText = text.replace(/[^a-zA-Z0-9\s]/g, ""); // Filter out non-alphanumeric characters
    const lines = filteredText.split("\n");
    return lines.map((line, lineIndex) => ({
        line: lineIndex + 1,
        characters: line.split("").map((char, charIndex) => ({
            index: charIndex + 1,
            value: char,
        })),
    }));
}

// Display mapped text in the output container
function displayMappedText(jsonData) {
    const outputContainer = document.getElementById("outputContainer");
    const saveButton = document.querySelector(".save-text"); // Select the save button
    outputContainer.innerHTML = ""; // Clear previous content

    jsonData.forEach(line => {
        const lineContainer = document.createElement("div");
        lineContainer.className = "line-container";

        line.characters.forEach(charObj => {
            const span = document.createElement("span");
            span.className = "character-box";
            span.textContent = charObj.value;
            lineContainer.appendChild(span);
        });

        outputContainer.appendChild(lineContainer);
    });
    if (outputContainer.innerHTML.trim() !== "") {
        saveButton.style.display = "block"; // Show the button
    }
}

function displayImagePreview(imageUrl) {
    const filePreview = document.getElementById("filePreview");
    console.log("imageUrl" + imageUrl)
    if (imageUrl) {
        filePreview.innerHTML = `<img src="${imageUrl}" alt="Processed Image Preview">`;
    } else {
        filePreview.innerHTML = "No image preview available.";
    }
}

// Handle file input change event
document.getElementById("fileInput").addEventListener("change", event => {
    const file = event.target.files[0];
    if (file) {
        sendFileToBackend(file);
        closeModal();
    } else {
        alert("No file selected!");
    }
});

// Close modal if user clicks outside of it
window.onclick = function (event) {
    const modal = document.getElementById("uploadModal");
    if (event.target === modal) {
        closeModal();
    }
};

function redToHome(event) {
    window.location.href = "/"
}

function saveTextToFile() {
    const textContainer = document.getElementById("outputContainer");
    const textContent = textContainer.innerText || "";

    if (!textContent) {
        alert("No text available to save.");
        return;
    }

    const blob = new Blob([textContent], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "output.txt";
    link.click();
}
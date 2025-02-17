async function generateCaption() {
    let fileInput = document.getElementById("imageInput");
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    let response = await fetch("/caption", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    document.getElementById("captionResult").innerText = "Generated Caption: " + data.caption;
}

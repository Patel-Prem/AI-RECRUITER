// "use strict";

// const serverUrl = "http://127.0.0.1:8000";

// async function uploadfiles() {
//     // Check if any file is selected
//     if (!document.querySelectorAll('.doc')[0].files[0]) {
//       alert("Please select a file.");
//       return;
//     }
  
//     // Initialize an array to hold all the file promises
//     let filePromises = [];
//     let selectedFileNames = [];
//     // Loop through each file input with class "doc"
//     document.querySelectorAll('.doc').forEach(input => {
//       let file = input.files[0];
//       selectedFileNames.push(file.name);
//       // Push the promise for encoding file to the array
//       filePromises.push(new Promise(function(resolve, reject) {
//         const reader = new FileReader();
//         reader.readAsDataURL(file);
//         reader.onload = () => resolve({
//           fileName: file.name,
//           fileType: file.type, // Add file type here
//           fileBytes: reader.result.toString().replace(/^data:(.*,)?/, '')
//         });
//         reader.onerror = (error) => reject(error);
//       }));
//       // Clear file upload input field
//       // input.value = null;
//     });
  
//     // Wait for all files to be encoded
//     let encodedFiles = await Promise.all(filePromises);
  
//     // Make server call to upload image
//     // and return the server upload promise
//     return fetch(serverUrl + "/uploadfiles", {
//       method: "POST",
//       headers: {
//         'Accept': 'application/json',
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({
//         files: encodedFiles,
//         // filenames: filenames
//       })
//     }).then(response => {
//       if (response.ok) {
//         return response.json();
//       } else {
//         throw new HttpError(response);
//       }
//     });
//   }
  
// window.addEventListener('beforeunload', function(event) {
//     const fileInputs = document.querySelectorAll('.doc');
//     fileInputs.forEach(input => {
//         input.value = ''; // Reset the input field
//         localStorage.removeItem(input.id); // Remove any saved file names from localStorage
//     });
// });

// async function readFiles(files) {
//   const response = await fetch(serverUrl + "/readfiles", {
//     method: "POST",
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ jdResumeURI: { "jdURI": files[0]["fileUrl"], "resumeURI": files[1]["fileUrl"], "videoURI": files[2]["fileUrl"] } })
//   });
//   if (response.ok) {
//     return response.json();
//   } else {
//     throw new HttpError(response);
//   }
// }

// function convertToPercentage(arr) {
//   let total = 0;
//   for (const i of arr) {
//     total += i;
//   }
//   if (arr.length > 1)
//     return (total / arr.length).toFixed(2).padStart(5, 0) + '%';

//   return total.toFixed(2).padStart(5, 0) + '%';
// }

// function embedSimilarity(similarities) {
//   let resume_similarity = convertToPercentage([similarities['resume_similarity']['combine_skills']])
//   let interview_similarity = convertToPercentage([similarities['video_similarity']['combine_skills']])
//   let avg_hard_skill = convertToPercentage([similarities['video_similarity']['hard_skills'], similarities['resume_similarity']['hard_skills']])
//   let avg_soft_skill = convertToPercentage([similarities['video_similarity']['soft_skills'], similarities['resume_similarity']['soft_skills']])

//   console.log('resume_similarity', resume_similarity)
//   console.log('interview_similarity',  interview_similarity)
//   console.log('avg_hard_skill',  avg_hard_skill)
//   console.log('avg_soft_skill',  avg_soft_skill)
  
//   document.getElementById("resumeProgress").style.width = resume_similarity;
//   document.getElementById("interviewProgress").style.width = interview_similarity;
//   document.getElementById("hardSkillsProgress").style.width = avg_hard_skill;
//   document.getElementById("softSkillsProgress").style.width = avg_soft_skill;

//   document.getElementById("resumeProgressPercentage").innerText = resume_similarity;
//   document.getElementById("interviewProgressPercentage").innerText = interview_similarity;
//   document.getElementById("hardSkillsProgressPercentage").innerHTML = avg_hard_skill;
//   document.getElementById("softSkillsProgressPercentage").innerHTML = avg_soft_skill;
// }

// function uploadAndTranslate() {
//     const spinner = document.getElementById("loader");
//     const submitButton = document.querySelector('button[type="submit"]');
    
//     // Disable submit button and show loader
//     submitButton.disabled = true;
//     spinner.classList.remove("d-none");
  
//     uploadfiles()
//       .then(files => readFiles(files))
//       .then(similarities => {
//         embedSimilarity(similarities);
//         spinner.classList.add("d-none");
//         // Enable submit button after results are received
//         submitButton.disabled = false;
//       })
//       .catch(error => {
//         spinner.classList.add("d-none");
//         submitButton.disabled = false;
//         alert("Error: " + error);
//       });
// }

// class HttpError extends Error {
//   constructor(response) {
//     super(`${response.status} for ${response.url}`);
//     this.name = "HttpError";
//     this.response = response;
//   }
// }



"use strict";

const serverUrl = "http://127.0.0.1:8000";

function checkextension(fileInput, errorMessage, allowedExtensionsRegex) {
  if (!fileInput || !allowedExtensionsRegex) return;
  const filePath = fileInput.value; 
    
  if (!allowedExtensionsRegex.exec(filePath)) {
      alert(errorMessage)
      fileInput.value = '';
  } 
}

function checkextensionPdf(inputFile, errorMessage) {
  const pdfRegex = /(\.pdf)$/i;
  return checkextension(inputFile, errorMessage, pdfRegex);
}

function checkextensionMp4(inputFile, errorMessage) {
  const mp4Regex = /(\.mp4)$/i;
  return checkextension(inputFile, errorMessage, mp4Regex);
}

async function uploadfiles() {
    // Check if any file is selected
    if (!document.querySelectorAll('.doc')[0].files[0]) {
      alert("Please select a file.");
      return;
    }
  
    // Initialize an array to hold all the file promises
    let filePromises = [];
    let selectedFileNames = [];
    // Loop through each file input with class "doc"
    document.querySelectorAll('.doc').forEach(input => {
      let file = input.files[0];
      selectedFileNames.push(file.name);
      // Push the promise for encoding file to the array
      filePromises.push(new Promise(function(resolve, reject) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve({
          fileName: file.name,
          fileType: file.type, // Add file type here
          fileBytes: reader.result.toString().replace(/^data:(.*,)?/, '')
        });
        reader.onerror = (error) => reject(error);
      }));
      // Clear file upload input field
      // input.value = null;
    });
  
    // Wait for all files to be encoded
    let encodedFiles = await Promise.all(filePromises);
  
    // Make server call to upload image
    // and return the server upload promise
    return fetch(serverUrl + "/uploadfiles", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        files: encodedFiles,
        // filenames: filenames
      })
    }).then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new HttpError(response);
      }
    });
  }
  
window.addEventListener('beforeunload', function(event) {
    const fileInputs = document.querySelectorAll('.doc');
    fileInputs.forEach(input => {
        input.value = ''; // Reset the input field
        localStorage.removeItem(input.id); // Remove any saved file names from localStorage
    });
});

async function readFiles(files) {
  const response = await fetch(serverUrl + "/readfiles", {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ jdResumeURI: { "jdURI": files[0]["fileUrl"], "resumeURI": files[1]["fileUrl"], "videoURI": files[2]["fileUrl"] } })
  });
  if (response.ok) {
    return response.json();
  } else {
    throw new HttpError(response);
  }
}

async function translateVideo(video) {
    // console.log('videovideovideo', video)
    // Array(3) [ {…}, {…}, {…} ]
    // 0: Object { fileId: "Job Discription.pdf", fileUrl: "http://contentcen301298810.aws.ai.s3.amazonaws.com/Job Discription.pdf" }
    // ​
    // 1: Object { fileId: "OHM PATEL Resume.pdf", fileUrl: "http://contentcen301298810.aws.ai.s3.amazonaws.com/OHM PATEL Resume.pdf" }
    // ​
    // 2: Object { fileId: "Scenario 1_ Related to Job Description.mp4", fileUrl: "http://contentcen301298810.aws.ai.s3.amazonaws.com/Scenario 1_ Related to Job Description.mp4" }
    // ​​
    // fileId: "Scenario 1_ Related to Job Description.mp4"
    // ​​
    // fileUrl: "http://contentcen301298810.aws.ai.s3.amazonaws.com/Scenario 1_ Related to Job Description.mp4"

    // for video video[2]["fileUrl"]
    return await fetch(serverUrl + "/video/translate-text", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({LanguageCode: "en-US", URI: video[2]["fileUrl"]})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function convertToPercentage(arr) {
  let total = 0;
  for (const i of arr) {
    total += i;
  }
  if (arr.length > 1)
    return (total / arr.length).toFixed(2).padStart(5, 0) + '%';

  return total.toFixed(2).padStart(5, 0) + '%';
}

function embedSimilarity(similarities) {
  let resume_similarity = convertToPercentage([similarities['resume_similarity']['combine_skills']])
  let interview_similarity = convertToPercentage([similarities['video_similarity']['combine_skills']])
  let avg_hard_skill = convertToPercentage([similarities['video_similarity']['hard_skills'], similarities['resume_similarity']['hard_skills']])
  let avg_soft_skill = convertToPercentage([similarities['video_similarity']['soft_skills'], similarities['resume_similarity']['soft_skills']])

  console.log('resume_similarity', resume_similarity)
  console.log('interview_similarity',  interview_similarity)
  console.log('avg_hard_skill',  avg_hard_skill)
  console.log('avg_soft_skill',  avg_soft_skill)
  
  document.getElementById("resumeProgress").style.width = resume_similarity;
  document.getElementById("interviewProgress").style.width = interview_similarity;
  document.getElementById("hardSkillsProgress").style.width = avg_hard_skill;
  document.getElementById("softSkillsProgress").style.width = avg_soft_skill;

  document.getElementById("resumeProgressPercentage").innerText = resume_similarity;
  document.getElementById("interviewProgressPercentage").innerText = interview_similarity;
  document.getElementById("hardSkillsProgressPercentage").innerHTML = avg_hard_skill;
  document.getElementById("softSkillsProgressPercentage").innerHTML = avg_soft_skill;
}

function uploadAndTranslate() {
    const spinner = document.getElementById("loader");
    const submitButton = document.querySelector('button[type="submit"]');
    
    // Disable submit button and show loader
    submitButton.disabled = true;
    spinner.classList.remove("d-none");
  
    uploadfiles()
      .then(files => readFiles(files))
      .then(similarities => {
        embedSimilarity(similarities);
        spinner.classList.add("d-none");
        // Enable submit button after results are received
        submitButton.disabled = false;
      })
      .catch(error => {
        spinner.classList.add("d-none");
        submitButton.disabled = false;
        alert("Error: " + error);
      });
}

class HttpError extends Error {
  constructor(response) {
    super(`${response.status} for ${response.url}`);
    this.name = "HttpError";
    this.response = response;
  }
}

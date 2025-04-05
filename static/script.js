// Initialize all editors
document.addEventListener("DOMContentLoaded", function () {
    // Hide error message initially
    document.getElementById("fileError").style.display = "none";

    // Load saved content for each editor
    document.querySelectorAll(".rich-text-editor").forEach((editor) => {
      const storageKey = editor.getAttribute("data-storage-key");
      const savedContent = localStorage.getItem(storageKey);
      if (savedContent) {
        editor.innerHTML = savedContent;
        // Update corresponding hidden input
        document.getElementById(`${storageKey}-hidden`).value =
          savedContent;
      }

      // Add input event listener to save content
      editor.addEventListener("input", function () {
        const content = this.innerHTML;
        localStorage.setItem(storageKey, content);
        document.getElementById(`${storageKey}-hidden`).value = content;
      });
    });

    // Add toolbar button functionality
    document
      .querySelectorAll(".editor-toolbar button")
      .forEach((button) => {
        button.addEventListener("click", function (e) {
          e.preventDefault();
          const command = this.getAttribute("data-command");
          document.execCommand(command, false, null);

          // Update active state
          updateButtonState(this, command);
        });

        // Touch support for mobile
        button.addEventListener(
          "touchstart",
          function (e) {
            e.preventDefault();
            const command = this.getAttribute("data-command");
            document.execCommand(command, false, null);

            // Update active state
            updateButtonState(this, command);
          },
          { passive: false }
        );
      });

    // Function to update button active state
    function updateButtonState(button, command) {
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const parentElement = range.commonAncestorContainer.parentElement;

        if (command === "bold") {
          button.classList.toggle(
            "active",
            parentElement.tagName === "B" ||
              parentElement.tagName === "STRONG"
          );
        } else if (command === "italic") {
          button.classList.toggle(
            "active",
            parentElement.tagName === "I" || parentElement.tagName === "EM"
          );
        } else if (command === "underline") {
          button.classList.toggle("active", parentElement.tagName === "U");
        }
      }
    }
  });

  function allowed_file(filename) {
    const allowedExtensions = ["png", "jpg", "jpeg"];
    const fileExtension = filename.split(".").pop().toLowerCase();
    return allowedExtensions.includes(fileExtension);
  }

  document.getElementById("logo").addEventListener("change", function (e) {
    const file = e.target.files[0];
    const fileError = document.getElementById("fileError");

    if (!file || !allowed_file(file.name)) {
      fileError.style.display = "block";
      e.target.value = "";
    } else {
      fileError.style.display = "none";
    }
  });

  function clearStorage() {
    Swal.fire({
      title: "Konfirmasi",
      text: "Apakah Anda yakin ingin menghapus semua data tersimpan?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Ya, hapus!",
      cancelButtonText: "Batal",
    }).then((result) => {
      if (result.isConfirmed) {
        localStorage.clear();
        document.querySelectorAll(".rich-text-editor").forEach((editor) => {
          editor.innerHTML = "";
          // Also clear the hidden inputs
          const storageKey = editor.getAttribute("data-storage-key");
          document.getElementById(`${storageKey}-hidden`).value = "";
        });
        document.getElementById("proposalForm").reset();
        Swal.fire("Dihapus!", "Data tersimpan telah dihapus.", "success");
      }
    });
  }

  async function handleGenerate() {
    const form = document.getElementById("proposalForm");
    const formData = new FormData(form);

    // Validate all fields
    let isValid = true;
    let firstEmptyField = null;

    const editors = document.querySelectorAll(".rich-text-editor");
    editors.forEach((editor) => {
      if (!editor.innerHTML.trim()) {
        isValid = false;
        editor.style.border = "1px solid red";
        if (!firstEmptyField) {
          firstEmptyField = editor;
        }
      } else {
        editor.style.border = "1px solid #ddd";
      }
    });

    const fileInput = document.getElementById("logo");
    if (!fileInput.files || fileInput.files.length === 0) {
      isValid = false;
      fileInput.style.border = "1px solid red";
      if (!firstEmptyField) {
        firstEmptyField = fileInput;
      }
    } else {
      fileInput.style.border = "";
    }

    if (!isValid) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Harap isi semua field yang wajib diisi!",
      });
      if (firstEmptyField) {
        if (firstEmptyField === fileInput) {
          firstEmptyField.focus();
        } else {
          firstEmptyField.focus();
          // Untuk contenteditable div, kita perlu set selection range
          const range = document.createRange();
          const sel = window.getSelection();
          range.selectNodeContents(firstEmptyField);
          range.collapse(true);
          sel.removeAllRanges();
          sel.addRange(range);
        }
      }
      return;
    }

    try {
      // Show loading state
      const generateBtn = document.querySelector(".btn-generate");
      generateBtn.disabled = true;
      generateBtn.textContent = "Memproses...";

      const response = await fetch("/generate", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error ||
            "Terjadi kesalahan saat mengirim data ke server."
        );
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "proposal.docx";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      Swal.fire({
        icon: "success",
        title: "Berhasil!",
        text: "Proposal berhasil di-generate.",
      });
    } catch (error) {
      console.error("Terjadi kesalahan:", error);
      Swal.fire({
        icon: "error",
        title: "Terjadi Kesalahan",
        text: error.message,
      });
    } finally {
      // Reset button state
      const generateBtn = document.querySelector(".btn-generate");
      generateBtn.disabled = false;
      generateBtn.textContent = "Generate Proposal";
    }
  }// Initialize all editors
document.addEventListener("DOMContentLoaded", function () {
    // Hide error message initially
    document.getElementById("fileError").style.display = "none";

    // Load saved content for each editor
    document.querySelectorAll(".rich-text-editor").forEach((editor) => {
      const storageKey = editor.getAttribute("data-storage-key");
      const savedContent = localStorage.getItem(storageKey);
      if (savedContent) {
        editor.innerHTML = savedContent;
        // Update corresponding hidden input
        document.getElementById(`${storageKey}-hidden`).value =
          savedContent;
      }

      // Add input event listener to save content
      editor.addEventListener("input", function () {
        const content = this.innerHTML;
        localStorage.setItem(storageKey, content);
        document.getElementById(`${storageKey}-hidden`).value = content;
      });
    });

    // Add toolbar button functionality
    document
      .querySelectorAll(".editor-toolbar button")
      .forEach((button) => {
        button.addEventListener("click", function (e) {
          e.preventDefault();
          const command = this.getAttribute("data-command");
          document.execCommand(command, false, null);

          // Update active state
          updateButtonState(this, command);
        });

        // Touch support for mobile
        button.addEventListener(
          "touchstart",
          function (e) {
            e.preventDefault();
            const command = this.getAttribute("data-command");
            document.execCommand(command, false, null);

            // Update active state
            updateButtonState(this, command);
          },
          { passive: false }
        );
      });

    // Function to update button active state
    function updateButtonState(button, command) {
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const parentElement = range.commonAncestorContainer.parentElement;

        if (command === "bold") {
          button.classList.toggle(
            "active",
            parentElement.tagName === "B" ||
              parentElement.tagName === "STRONG"
          );
        } else if (command === "italic") {
          button.classList.toggle(
            "active",
            parentElement.tagName === "I" || parentElement.tagName === "EM"
          );
        } else if (command === "underline") {
          button.classList.toggle("active", parentElement.tagName === "U");
        }
      }
    }
  });

  function allowed_file(filename) {
    const allowedExtensions = ["png", "jpg", "jpeg"];
    const fileExtension = filename.split(".").pop().toLowerCase();
    return allowedExtensions.includes(fileExtension);
  }

  document.getElementById("logo").addEventListener("change", function (e) {
    const file = e.target.files[0];
    const fileError = document.getElementById("fileError");

    if (!file || !allowed_file(file.name)) {
      fileError.style.display = "block";
      e.target.value = "";
    } else {
      fileError.style.display = "none";
    }
  });

  function clearStorage() {
    Swal.fire({
      title: "Konfirmasi",
      text: "Apakah Anda yakin ingin menghapus semua data tersimpan?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Ya, hapus!",
      cancelButtonText: "Batal",
    }).then((result) => {
      if (result.isConfirmed) {
        localStorage.clear();
        document.querySelectorAll(".rich-text-editor").forEach((editor) => {
          editor.innerHTML = "";
          // Also clear the hidden inputs
          const storageKey = editor.getAttribute("data-storage-key");
          document.getElementById(`${storageKey}-hidden`).value = "";
        });
        document.getElementById("proposalForm").reset();
        Swal.fire("Dihapus!", "Data tersimpan telah dihapus.", "success");
      }
    });
  }

  async function handleGenerate() {
    const form = document.getElementById("proposalForm");
    const formData = new FormData(form);

    // Validate all fields
    let isValid = true;
    let firstEmptyField = null;

    const editors = document.querySelectorAll(".rich-text-editor");
    editors.forEach((editor) => {
      if (!editor.innerHTML.trim()) {
        isValid = false;
        editor.style.border = "1px solid red";
        if (!firstEmptyField) {
          firstEmptyField = editor;
        }
      } else {
        editor.style.border = "1px solid #ddd";
      }
    });

    const fileInput = document.getElementById("logo");
    if (!fileInput.files || fileInput.files.length === 0) {
      isValid = false;
      fileInput.style.border = "1px solid red";
      if (!firstEmptyField) {
        firstEmptyField = fileInput;
      }
    } else {
      fileInput.style.border = "";
    }

    if (!isValid) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Harap isi semua field yang wajib diisi!",
      });
      if (firstEmptyField) {
        if (firstEmptyField === fileInput) {
          firstEmptyField.focus();
        } else {
          firstEmptyField.focus();
          // Untuk contenteditable div, kita perlu set selection range
          const range = document.createRange();
          const sel = window.getSelection();
          range.selectNodeContents(firstEmptyField);
          range.collapse(true);
          sel.removeAllRanges();
          sel.addRange(range);
        }
      }
      return;
    }

    try {
      // Show loading state
      const generateBtn = document.querySelector(".btn-generate");
      generateBtn.disabled = true;
      generateBtn.textContent = "Memproses...";

      const response = await fetch("/generate", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error ||
            "Terjadi kesalahan saat mengirim data ke server."
        );
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "proposal.docx";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      Swal.fire({
        icon: "success",
        title: "Berhasil!",
        text: "Proposal berhasil di-generate.",
      });
    } catch (error) {
      console.error("Terjadi kesalahan:", error);
      Swal.fire({
        icon: "error",
        title: "Terjadi Kesalahan",
        text: error.message,
      });
    } finally {
      // Reset button state
      const generateBtn = document.querySelector(".btn-generate");
      generateBtn.disabled = false;
      generateBtn.textContent = "Generate Proposal";
    }
  }
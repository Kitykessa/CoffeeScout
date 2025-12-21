// ======= FLAVOR PROFILE BARS & AVG NOTES =======
const flavorSection = document.getElementById("flavorProfileSection");

if (flavorSection) {
  const avgData = JSON.parse(flavorSection.dataset.avg || "{}");
  const maxHeight = 160; // повна висота контуру у px

  const labels = ["Aroma", "Acidity", "Bitterness", "Body", "Finish", "Roast"];

  labels.forEach(label => {
    const val = avgData[label.toLowerCase()] || 0;

    const outline = document.getElementById("bar-" + label);
    if (!outline) return;

    const fill = outline.querySelector(".bar-fill");
    const tooltip = outline.querySelector(".bar-tooltip");

    fill.style.height = (val / 10 * maxHeight) + "px";
    tooltip.textContent = Math.round(val * 10) + "%";
  });
}



// ======= AVG NOTES (унікальні + кількість) =======
const avgNotesContainer = document.getElementById("avgNotesDisplay");
if (avgNotesContainer) {
  const notesData = JSON.parse(avgNotesContainer.dataset.notes || "[]");
  const noteCounts = JSON.parse(avgNotesContainer.dataset.counts || "{}");

  const buttonsContainer = avgNotesContainer.querySelector(".notes-buttons");

  // очищаємо, щоб не дублювати
  buttonsContainer.innerHTML = "";

  [...new Set(notesData)].forEach(note => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tag-btn";
    btn.textContent = note;
    btn.disabled = true;

    // tooltip через title або окремий span
    btn.title = `${noteCounts[note]} user(s) voted`;

    buttonsContainer.appendChild(btn);
  });
}




// ======== 🟤 NOTES SELECTION (форма користувача) ========
let selectedNotes = [];
const tagButtons = document.querySelectorAll("#noteTags .tag-btn");
const notesHidden = document.getElementById("notes_hidden");
const addNoteBtn = document.getElementById("addNoteBtn");
const customNoteInput = document.getElementById("custom_note");

// обробка натискання на існуючі кнопки
tagButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    btn.classList.toggle("active");
    const note = btn.textContent.trim();
    if (btn.classList.contains("active")) {
      if (!selectedNotes.includes(note)) selectedNotes.push(note);
    } else {
      selectedNotes = selectedNotes.filter(n => n !== note);
    }
    if (notesHidden) notesHidden.value = JSON.stringify(selectedNotes);
  });
});

// додавання власної нотки
if (addNoteBtn && customNoteInput) {
  addNoteBtn.addEventListener("click", () => {
    const custom = customNoteInput.value.trim();
    if (!custom) return;

    if (!selectedNotes.includes(custom)) {
      selectedNotes.push(custom);
      if (notesHidden) notesHidden.value = JSON.stringify(selectedNotes);

      const newBtn = document.createElement("button");
      newBtn.type = "button";
      newBtn.className = "tag-btn active";
      newBtn.textContent = custom;

      newBtn.addEventListener("click", () => {
        newBtn.classList.toggle("active");
        if (newBtn.classList.contains("active")) {
          selectedNotes.push(custom);
        } else {
          selectedNotes = selectedNotes.filter(n => n !== custom);
        }
        if (notesHidden) notesHidden.value = JSON.stringify(selectedNotes);
      });

      const container = document.getElementById("noteTags");
      container.appendChild(newBtn);
    }
    customNoteInput.value = "";
  });
}


// ======== 🟤 CIRCLE SLIDERS (visual fill) ========
const circleGroups = document.querySelectorAll(".circle-slider");
circleGroups.forEach(group => {
  const inputs = Array.from(group.querySelectorAll("input"));
  const labels = Array.from(group.querySelectorAll("label"));

  const paint = (value) => {
    labels.forEach((lbl, idx) => {
      if (idx < value) {
        lbl.style.backgroundColor = "#8B4513";
        lbl.style.transform = "scale(1.08)";
      } else {
        lbl.style.backgroundColor = "#e0c4a8";
        lbl.style.transform = "scale(1)";
      }
    });
  };

  inputs.forEach(input => {
    input.addEventListener("change", () => {
      paint(Number(input.value));
    });

    if (input.checked) paint(Number(input.value));
  });
});


// ======== ☕ ROAST LEVEL SLIDER ========
const roastDots = document.querySelectorAll(".roast-dots input");
const roastLabels = document.querySelectorAll(".roast-dots label");
roastDots.forEach(dot => {
  dot.addEventListener("change", () => {
    const value = parseInt(dot.value);
    roastLabels.forEach((lbl, idx) => {
      if (idx < value) {
        lbl.style.backgroundColor = "#8B4513";
        lbl.style.transform = "scale(1.08)";
      } else {
        lbl.style.backgroundColor = "#ffffff48";
        lbl.style.transform = "scale(1)";
      }
    });
  });

  if (dot.checked) {
    const v = parseInt(dot.value);
    roastLabels.forEach((lbl, idx) => {
      lbl.style.backgroundColor = (idx < v) ? "#8B4513" : "#ffffff48";
    });
  }
});


// ======== 🟤 SAVE FLAVOR PROFILE (submit) ========
const saveFlavorBtn = document.getElementById("saveFlavorBtn");
if (saveFlavorBtn) {
  saveFlavorBtn.addEventListener("click", () => {
    const form = saveFlavorBtn.closest("form");
    if (form) form.submit();
  });
}

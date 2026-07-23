const MIN_LENGTH = 1;
const MAX_LENGTH = 100;
// Must mirror the backend allow-list in app.py (is_valid_search_term).
const ALLOWED_PATTERN = /^[A-Za-z0-9 ,.\-_]+$/;

function validateSearchForm() {
  const field = document.getElementById("search_term");
  const value = field.value.trim();

  if (value.length < MIN_LENGTH || value.length > MAX_LENGTH || !ALLOWED_PATTERN.test(value)) {
    field.value = "";
    alert("Invalid search term. Use only letters, numbers, spaces, and , . - _");
    return false;
  }
  return true;
}

// Exposed for the inline onsubmit="" handler in home.html
globalThis.validateSearchForm = validateSearchForm;

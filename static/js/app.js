function showLoading() {
  const button = document.getElementById("generateButton");
  const loading = document.getElementById("loading");
  if (button) {
    button.disabled = true;
    button.innerHTML = "Creating…";
  }
  if (loading) loading.hidden = false;
}
